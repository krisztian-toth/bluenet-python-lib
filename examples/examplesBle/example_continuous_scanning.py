#!/usr/bin/env python3

"""An example that scans for your Crownstones"""

import time

from BluenetLib.BLE import BluenetBle
from BluenetLib import BluenetEventBus, Topics


# Function that's called when the power usage is updated.
def showData(data):
	print("data", data["address"], data["rssi"], data["serviceData"]["setupMode"])


# Set up event listeners
BluenetEventBus.subscribe(Topics.advertisement, showData)

# Initialize the Bluetooth Core.
# Fill in the correct hciIndex, see the readme.
# Fill in the correct keys, see the readme.
core = BluenetBle(hciIndex=0)
core.setSettings("adminKeyForCrown", "memberKeyForHome", "guestKeyForOther")


print("Scanning for Crownstones..")
core.startScanning(60)

core.shutDown()