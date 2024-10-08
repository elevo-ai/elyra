<!--
{% comment %}
This program is an unpublished work fully protected by the United States
copyright laws and is considered a trade secret belonging to Elevo Corporation.
To the extent that this work may be considered "published", the following notice applies
"(C) 2020, 2023, Elevo Corporation"

Any unauthorized use, reproduction, distribution, display, modification,
or disclosure of this program is strictly prohibited.

Copyright 2018-2022 Elyra Authors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
{% endcomment %}
-->

# Instructions to build foresight/elyra jupyter distributions

## One-time setup

### Dependencies:
   - Get Miniconda for python3 (https://docs.conda.io/en/latest/miniconda.html). Use the Python 3 Linux x86_64 installer,
     which is a shell script you download.
   - Install using the command ([Help](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html))
     ```
     bash Miniconda3-latest-Linux-x86_64.sh
     ```
   - Initialize conda, either in the installer or later, using this command:
     ```
     conda init
     ```
   - Remove the code that conda init adds to your `~/.bashrc` and move it to a separate script.
     Only source that code when you actually want to use miniconda and not our regular Python environment.
     Make sure you don't have the `PYTHONPATH` env variable set or activated a regular Python venv when using miniconda.
      
### Create conda venv:
```
conda create -n <env-name> python==3.7.9
```

### Install required packages inside conda venv:
   - Activate previous created conda venv
     ```
     conda activate <env-name>
     ```
   - Install nodejs
     ```
     conda install -y -c conda-forge/label/main nodejs
     ```
   - Install yarn
     ```
     conda install -y -c conda-forge/label/main yarn
     ```
   - Install the black code formatter
     ```
     conda install -y black
     ```
   - git clone eleoai/elyra
     ```
     git clone https://github.com/elevo-ai/elyra
     cd elyra
     ```

## Commands done once per build

   - run the create_foresight_release.py python script to build the foresight dependency files
     ```
     conda activate <env-name>
     cd elyra
     python create_foresight_release.py prepare --version 3.15.0.dev0
     ```

     Note: 
     All distributable files will be created in dist folder. Please copy
     the  *.whl files and *extension* files to foresight location for validation 
     with foresight product
