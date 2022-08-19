#!/usr/bin/env python3
import argparse
import elyra
import elyra._version
# import git
import io
import os
import re
import shutil
import subprocess
import sys

from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

config: SimpleNamespace

VERSION_REG_EX = r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(\.(?P<pre_release>[a-z]+)(?P<build>\d+))?"


class DependencyException(Exception):
    """Error if dependency is missing"""


class MissingReleaseArtifactException(Exception):
    """Error if an artifact being released is not available"""


class UpdateVersionException(Exception):
    """Error if the old version is invalid or cannot be found, or if there's a duplicate version"""


def check_run(args, cwd=os.getcwd(), capture_output=True, env=None, shell=False) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(args, cwd=cwd, capture_output=capture_output, check=True)
    except subprocess.CalledProcessError as ex:
        raise RuntimeError(f'Error executing process: {ex.stderr.decode("unicode_escape")}') from ex


def check_output(args, cwd=os.getcwd(), env=None, shell=False) -> str:
    response = check_run(args, cwd, capture_output=True, env=env, shell=shell)
    return response.stdout.decode("utf-8").replace("\n", "")


def dependency_exists(command) -> bool:
    """Returns true if a command exists on the system"""
    try:
        check_run(["which", command])
    except subprocess.CalledProcessError:
        return False

    return True


def sed(file: str, pattern: str, replace: str) -> None:
    """Perform regex substitution on a given file"""
    try:
        check_run(["sed", "-i", "", "-e", f"s#{pattern}#{replace}#g", file], capture_output=False)
    except Exception as ex:
        raise RuntimeError(f"Error processing updated to file {file}: ") from ex


def validate_dependencies() -> None:
    """Error if a dependency is missing or invalid"""
    if not dependency_exists("node"):
        raise DependencyException("Please install node.js v16+ https://nodejs.org/")
    if not dependency_exists("yarn"):
        raise DependencyException("Please install yarn https://classic.yarnpkg.com/")


def _source(file: str) -> str:
    global config

    return os.path.join(config.source_dir, file)


def build_server():
    global config

    print("-----------------------------------------------------------------")
    print("------------------------ Building Server ------------------------")
    print("-----------------------------------------------------------------")

    # update project name
    sed(_source("setup.py"), r'name="elyra"', 'name="elyra-server"')
    sed(
        _source("setup.py"),
        r'description="Elyra provides AI Centric extensions to JupyterLab"',
        'description="The elyra/Integra-server package provides common core libraries and functions that are required by '
        "Elyra's individual extensions. Note: Installing this package alone will not enable the use of Elyra. "
        "Please install the 'elyra' package instead. e.g. pip install elyra[all]\"",
    )
    # install elyra
    check_run(["make", "clean" "install"], cwd=config.source_dir, capture_output=False)

    # build server wheel
    check_run(["make", "build-server"], cwd=config.source_dir, capture_output=False)


def copy_extension_dir(extension: str, work_dir: str) -> None:
    global config

    extension_package_source_dir = os.path.join(config.source_dir, "dist/labextensions/@elyra", extension)
    extension_package_dest_dir = os.path.join(work_dir, "dist/labextensions/@elyra", extension)
    os.makedirs(os.path.dirname(extension_package_dest_dir), exist_ok=True)
    shutil.copytree(extension_package_source_dir, extension_package_dest_dir)


def prepare_extensions_release() -> None:
    global config

    print("-----------------------------------------------------------------")
    print("--------------- Preparing Individual Extensions -----------------")
    print("-----------------------------------------------------------------")

    extensions = {
        "elyra-template-extension": SimpleNamespace(
            packages=["template-extension", "metadata-extension", "theme-extension"],
            description=f"The Template editor extension adds support for reusable code fragments, "
                        f"making programming in JupyterLab more efficient by reducing repetitive work. "
                        f"See https://elyra.readthedocs.io/en/v{config.new_version}/user_guide/templates.html",
        ),
        "elyra-code-snippet-extension": SimpleNamespace(
            packages=["code-snippet-extension", "metadata-extension", "theme-extension"],
            description=f"The code-snippet editor extension adds support for reusable code fragments, "
                        f"making programming in JupyterLab more efficient by reducing repetitive work. "
                        f"See https://elyra.readthedocs.io/en/v{config.new_version}/user_guide/code-snippets.html",
        ),

    }

    for extension in extensions:
        extension_source_dir = os.path.join(config.work_dir, extension)
        print(f"Preparing extension : {extension} at {extension_source_dir}")
        # copy extension package template to working directory
        if os.path.exists(extension_source_dir):
            print(f"Removing working directory: {config.source_dir}")
            shutil.rmtree(extension_source_dir)
        check_run(["mkdir", "-p", extension_source_dir], cwd=config.work_dir)
        print(f'Copying : {_source("etc/templates/setup.py")} to {extension_source_dir}')
        check_run(["cp", _source("etc/templates/setup.py"), extension_source_dir], cwd=config.work_dir)
        # update template
        setup_file = os.path.join(extension_source_dir, "setup.py")
        sed(setup_file, "{{package-name}}", extension)
        sed(setup_file, "{{version}}", config.new_version)
        sed(setup_file, "{{data - files}}", re.escape("('share/jupyter/labextensions', 'dist/labextensions', '**')"))
        sed(setup_file, "{{install - requires}}", f"'elyra-server=={config.new_version}',")
        sed(setup_file, "{{description}}", f"'{extensions[extension].description}'")

        for dependency in extensions[extension].packages:
            copy_extension_dir(dependency, extension_source_dir)

        # build extension
        check_run(["python", "setup.py", "bdist_wheel", "sdist"], cwd=extension_source_dir)
        print("")


def prepare_release() -> None:
    """
    Prepare a release
    """
    global config
    print(f"Processing release from {config.old_version} to {config.new_version} ")
    print("")

    # server-only wheel
    build_server()

    # prepare extensions
    prepare_extensions_release()


def initialize_config(args=None) -> SimpleNamespace:
    if not args:
        raise ValueError("Invalid command line arguments")

    v = re.search(VERSION_REG_EX, elyra._version.__version__)

    configuration = {
        "goal": args.goal,
        "base_dir": os.getcwd(),
        "work_dir": os.path.join(os.getcwd()),
        "source_dir": os.path.join(os.getcwd()),
        "new_version": args.version
    }

    global config
    config = SimpleNamespace(**configuration)


def print_config() -> None:
    global config
    print("")
    print("-----------------------------------------------------------------")
    print("--------------------- Release configuration ---------------------")
    print("-----------------------------------------------------------------")
    print(f"Goal \t\t\t -> {config.goal}")
    print(f"Work dir \t\t -> {config.work_dir}")
    print(f"Source dir \t\t -> {config.source_dir}")
    print(f"Version \t\t -> {config.new_version}")
    print("-----------------------------------------------------------------")
    print("")


def print_help() -> str:
    return """create-release.py [ prepare | publish ] --version VERSION

    DESCRIPTION
    Creates Elyra release based on git commit hash or from HEAD.

    create release prepare-changelog --version 1.3.0 [--beta 0] [--rc 0]
    This will prepare the release changelog and make it ready for review on the release workdir.

    create-release.py prepare --version 1.3.0 --dev-version 1.4.0 [--beta 0] [--rc 0]
    This will prepare a release candidate, build it locally and make it ready for review on the release workdir.

    Note: that one can either use a beta or rc modifier for the release, but not both.

    create-release.py publish --version 1.3.0 [--beta 0] [--rc 0]
    This will build a previously prepared release, and publish the artifacts to public repositories.

    Required software dependencies for building and publishing a release:
     - Git
     - Node
     - Twine
     - Yarn

     Required configurations for publishing a release:
     - GPG with signing key configured


    """


def main(args=None):
    """Perform necessary tasks to create and/or publish a new release"""
    parser = argparse.ArgumentParser(usage=print_help())
    parser.add_argument(
        "goal",
        help="Supported goals: {prepare-changelog | prepare | publish}",
        type=str,
        choices={"prepare-changelog", "prepare", "publish"},
    )
    parser.add_argument("--version", help="the new release version", type=str, required=True)
    args = parser.parse_args()

    global config
    try:
        # Validate all pre-requisites are available
        validate_dependencies()

        # Generate release config based on the provided arguments
        initialize_config(args)
        print_config()

        if config.goal == "prepare":

            prepare_release()

            print("")
            print("")
            print(f"Release version: {config.new_version} is ready for review")
            print("After you are done, run the script again to [publish] the release.")
            print("")
            print("")
        else:
            print_help()
            sys.exit()

    except Exception as ex:
        raise RuntimeError(f"Error performing release {args.version}") from ex


if __name__ == "__main__":
    main()
