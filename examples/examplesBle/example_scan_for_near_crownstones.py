#!/usr/bin/env python3

import time

from BluenetLib.BLE import BluenetBle

print("===========================================\n\nStarting Example\n\n===========================================")
print("This is an example that scans for any Crownstone, and prints the results.\n")

# Initialize the Bluetooth Core.
# Fill in the correct hciIndex, see the readme.
# Fill in the correct keys, see the readme.
core = BluenetBle(hciIndex=0)
core.setSettings("adminKeyForCrown", "memberKeyForHome", "guestKeyForOther")

print("Searching for Crownstones in range, this will take a while.")

crownstonesInRange = core.getCrownstonesByScanning()

for stoneInRange in crownstonesInRange:
    print(stoneInRange)

# clean up all pending processes
print("Core shutdown")
core.shutDown()

print("===========================================\n\nFinished Example\n\n===========================================")

