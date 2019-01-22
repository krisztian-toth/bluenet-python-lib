#!/usr/bin/env python3

"""An example that turns on a Crownstone with given MAC address."""

import time

from BluenetLib.BLE import BluenetBle

print("===========================================\n\nStarting Example\n\n===========================================")

# Initialize the Bluetooth Core.
# Fill in the correct hciIndex, see the readme.
# Fill in the correct keys, see the readme.
core = BluenetBle(hciIndex=0)
core.setSettings("adminKeyForCrown", "memberKeyForHome", "guestKeyForOther")

# Fill in the correct MAC address.
address = "d0:30:f7:32:b3:07"
print("Connecting to", address)

core.connect(address)
core.control.setSwitchState(1)
core.control.disconnect()

core.shutDown()

print("===========================================\n\nFinished Example\n\n===========================================")

