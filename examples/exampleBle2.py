#!/usr/bin/env python
import time

from BluenetLib.BLE import BluenetBle

print("===========================================\n\nStarting Example\n\n===========================================")

# initialize the Bluetooth Core
core = BluenetBle()
core.setSettings("adminKeyForCrown", "memberKeyForHome", "guestKeyForOther")

print("Searching for the nearest setup Crownstone")
# get the nearest crownstone in setup mode. We expect it to be atleast within the -70db range
crownstonesInRange = core.getCrownstonesByScanning()

print(crownstonesInRange)

# clean up all pending processes
print("Core shutdown")
core.shutDown()

print("===========================================\n\nFinished Example\n\n===========================================")

