#!/usr/bin/env python
import time

from BluenetLib.BLE import BluenetBle

print("===========================================\n\nStarting Example\n\n===========================================")

# initialize the Bluetooth Core
core = BluenetBle()
core.setSettings("adminKeyForCrown", "memberKeyForHome", "guestKeyForOther")

print("Searching for Crownstones in range")

crownstonesInRange = core.getCrownstonesByScanning()

for stoneInRange in crownstonesInRange:
    print(stoneInRange)

# clean up all pending processes
print("Core shutdown")
core.shutDown()

print("===========================================\n\nFinished Example\n\n===========================================")

