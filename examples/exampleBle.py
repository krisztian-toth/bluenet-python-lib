#!/usr/bin/env python
import time

from BluenetLib.BLE import BluenetBle

print("===========================================\n\nStarting Example\n\n===========================================")

# initialize the Bluetooth Core
core = BluenetBle()
core.setSettings("adminKeyForCrown", "memberKeyForHome", "guestKeyForOther")

print("Searching for the nearest setup Crownstone")
# get the nearest crownstone in setup mode. We expect it to be atleast within the -70db range
nearestStone = core.getNearestSetupCrownstone(rssiAtLeast=-70, returnFirstAcceptable=True)

print("Search Results:", nearestStone)

if nearestStone is not None:
    # setup the nearest Crownstone if we can find one
    print("Starting setup on ", nearestStone["address"])
    core.setupCrownstone(
        nearestStone["address"],
        crownstoneId=1,
        meshAccessAddress="4f745905",
        ibeaconUUID="1843423e-e175-4af0-a2e4-31e32f729a8a",
        ibeaconMajor=123,
        ibeaconMinor=456
    )
    
    # wait for setup to finish and the crownstone to reboot
    print("Sleeping until Crownstone is in Normal mode and ready.")
    time.sleep(10)
    
    # reset the Crownstone back into setup mode
    print("Starting the Factory Reset Process")
    core.connect(nearestStone["address"])
    print("Command factory reset")
    core.control.commandFactoryReset()
    print("command disconnect")
    core.control.disconnect()

# clean up all pending processes
print("Core shutdown")
core.shutDown()

print("===========================================\n\nFinished Example\n\n===========================================")