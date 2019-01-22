#!/usr/bin/env python3

"""An example that scans for your Crownstones"""

import time

from BluenetLib import BluenetBle
from BluenetLib import BluenetEventBus, Topics

import json

# Function that's called when new information is received from Crownstones with use the keys you provide in core.setSettings
def showNewData(data):
	print("New data received!")
	print(json.dumps(data, indent=2))
	print("-------------------")


# Set up event listeners
BluenetEventBus.subscribe(Topics.newDataAvailable, showNewData)

# Initialize the Bluetooth Core.
# Fill in the correct hciIndex, see the readme.
# Fill in the correct keys, see the readme.
core = BluenetBle(hciIndex=0)
core.setSettings("adminKeyForCrown", "memberKeyForHome", "guestKeyForOther")


print("Scanning for Crownstones..")
core.startScanning(60)
core.shutDown()