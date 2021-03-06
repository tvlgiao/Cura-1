# Copyright (c) 2015 Ultimaker B.V.
# Cura is released under the terms of the AGPLv3 or higher.

#Shoopdawoop
from . import CuraEngineBackend

from UM.i18n import i18nCatalog
catalog = i18nCatalog("cura")

def getMetaData():
    return {
        "plugin": {
            "name": "CuraEngine Backend",
            "author": "Ultimaker",
            "description": catalog.i18nc("CuraEngine backend plugin description", "Provides the link to the CuraEngine slicing backend"),
            "api": 2
        }
    }

def register(app):
    return { "backend": CuraEngineBackend.CuraEngineBackend() }

