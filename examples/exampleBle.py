#!/usr/bin/env python
import time
from BluenetLib.lib.core.BluetoothCore import BluetoothCore


print("\n\n\nStarting Example")

# initialize the Bluetooth Core
core = BluetoothCore()
core.setSettings("adminKeyForCrown", "memberKeyForHome", "guestKeyForOther")

#get the nearest crownstone in setup mode. We expect it to be atleast within the -70db range
nearestStone = core.getNearestSetupCrownstone(rssiAtLeast=-70, returnFirstAcceptable=True)

if nearestStone is not None:
    # setup the nearest Crownstone if we can find one
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
    core.control.commandFactoryReset()
    core.control.disconnect()

#clean up all pending processes
core.shutDown()

print("\n\n\nFinished Example")