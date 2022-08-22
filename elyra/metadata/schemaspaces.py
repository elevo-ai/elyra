#!/usr/bin/env python3
# ********************************************************************************************
#
# This program is an unpublished work fully protected by the United States
# copyright laws and is considered a trade secret belonging to Attala Systems Corporation.
# To the extent that this work may be considered "published", the following notice applies
# "(C) 2020, 2021, Attala Systems Corporation"
#
# Any unauthorized use, reproduction, distribution, display, modification,
# or disclosure of this program is strictly prohibited.
#
# ********************************************************************************************
from elyra.metadata.schema import Schemaspace


class Runtimes(Schemaspace):
    RUNTIMES_SCHEMASPACE_ID = "130b8e00-de7c-4b32-b553-b4a52824a3b5"
    RUNTIMES_SCHEMASPACE_NAME = "runtimes"
    RUNTIMES_SCHEMASPACE_DISPLAY_NAME = "Runtimes"

    def __init__(self, *args, **kwargs):
        super().__init__(
            schemaspace_id=Runtimes.RUNTIMES_SCHEMASPACE_ID,
            name=Runtimes.RUNTIMES_SCHEMASPACE_NAME,
            display_name=Runtimes.RUNTIMES_SCHEMASPACE_DISPLAY_NAME,
            description="Schemaspace for instances of Elyra runtime configurations",
        )


class RuntimeImages(Schemaspace):
    RUNTIME_IMAGES_SCHEMASPACE_ID = "119c9740-d73f-48c6-a97a-599d3acaf41d"
    RUNTIMES_IMAGES_SCHEMASPACE_NAME = "runtime-images"
    RUNTIMES_IMAGES_SCHEMASPACE_DISPLAY_NAME = "Runtime Images"

    def __init__(self, *args, **kwargs):
        super().__init__(
            schemaspace_id=RuntimeImages.RUNTIME_IMAGES_SCHEMASPACE_ID,
            name=RuntimeImages.RUNTIMES_IMAGES_SCHEMASPACE_NAME,
            display_name=RuntimeImages.RUNTIMES_IMAGES_SCHEMASPACE_DISPLAY_NAME,
            description="Schemaspace for instances of Elyra runtime images configurations",
        )


class CodeSnippets(Schemaspace):
    CODE_SNIPPETS_SCHEMASPACE_ID = "aa60988f-8f7c-4d09-a243-c54ef9c2f7fb"
    CODE_SNIPPETS_SCHEMASPACE_NAME = "code-snippets"
    CODE_SNIPPETS_SCHEMASPACE_DISPLAY_NAME = "Code Snippets"

    def __init__(self, *args, **kwargs):
        super().__init__(
            schemaspace_id=CodeSnippets.CODE_SNIPPETS_SCHEMASPACE_ID,
            name=CodeSnippets.CODE_SNIPPETS_SCHEMASPACE_NAME,
            display_name=CodeSnippets.CODE_SNIPPETS_SCHEMASPACE_DISPLAY_NAME,
            description="Schemaspace for instances of Elyra code snippets configurations",
        )


class Templates(Schemaspace):
    TEMPLATES_SCHEMASPACE_ID = "9b55e002-1cc6-11ed-861d-0242ac120002"
    TEMPLATES_SCHEMASPACE_NAME = "templates"
    TEMPLATES_SCHEMASPACE_DISPLAY_NAME = "Templates"

    def __init__(self, *args, **kwargs):
        super().__init__(
            schemaspace_id=Templates.TEMPLATES_SCHEMASPACE_ID,
            name=Templates.TEMPLATES_SCHEMASPACE_NAME,
            display_name=Templates.TEMPLATES_SCHEMASPACE_DISPLAY_NAME,
            description="Schemaspace for instances of Elyra templates configurations",
        )


class ComponentCatalogs(Schemaspace):
    COMPONENT_CATALOGS_SCHEMASPACE_ID = "8dc89ca3-4b90-41fd-adb9-9510ad346620"
    COMPONENT_CATALOGS_SCHEMASPACE_NAME = "component-catalogs"
    COMPONENT_CATALOGS_SCHEMASPACE_DISPLAY_NAME = "Component Catalogs"

    def __init__(self, *args, **kwargs):
        super().__init__(
            schemaspace_id=ComponentCatalogs.COMPONENT_CATALOGS_SCHEMASPACE_ID,
            name=ComponentCatalogs.COMPONENT_CATALOGS_SCHEMASPACE_NAME,
            display_name=ComponentCatalogs.COMPONENT_CATALOGS_SCHEMASPACE_DISPLAY_NAME,
            description="Schemaspace for instances of Elyra component catalog configurations",
        )
