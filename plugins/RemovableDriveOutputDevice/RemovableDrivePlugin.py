# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the AGPLv3 or higher.

import threading
import time

from UM.Signal import Signal
from UM.Message import Message
from UM.OutputDevice.OutputDevicePlugin import OutputDevicePlugin

from . import RemovableDriveOutputDevice

from UM.i18n import i18nCatalog
catalog = i18nCatalog("uranium")

class RemovableDrivePlugin(OutputDevicePlugin):
    def __init__(self):
        super().__init__()

        self._update_thread = threading.Thread(target = self._updateThread)
        self._update_thread.setDaemon(True)

        self._check_updates = True

        self._drives = {}

    def start(self):
        self._update_thread.start()

    def stop(self):
        self._check_updates = False
        self._update_thread.join()

        self._addRemoveDrives({})

    def checkRemovableDrives(self):
        raise NotImplementedError()

    def ejectDevice(self, device):
        result = self.performEjectDevice(device)
        if result:
            message = Message(catalog.i18n("Ejected {0}. You can now safely remove the drive.").format(device.getName()))
            message.show()
        else:
            message = Message(catalog.i18n("Failed to eject {0}. Maybe it is still in use?").format(device.getName()))
            message.show()

    def performEjectDevice(self, device):
        raise NotImplementedError()

    def _updateThread(self):
        while self._check_updates:
            result = self.checkRemovableDrives()
            self._addRemoveDrives(result)
            time.sleep(5)

    def _addRemoveDrives(self, drives):
        # First, find and add all new or changed keys
        for key, value in drives.items():
            if key not in self._drives:
                self.getOutputDeviceManager().addOutputDevice(RemovableDriveOutputDevice.RemovableDriveOutputDevice(key, value))
                continue

            if self._drives[key] != value:
                self.getOutputDeviceManager().removeOutputDevice(key)
                self.getOutputDeviceManager().addOutputDevice(RemovableDriveOutputDevice.RemovableDriveOutputDevice(key, value))

        # Then check for keys that have been removed
        for key in self._drives.keys():
            if key not in drives:
                self.getOutputDeviceManager().removeOutputDevice(key)

        self._drives = drives
