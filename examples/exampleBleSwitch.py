#!/usr/bin/env python
import time

from BluenetLib.BLE import BluenetBle

print("===========================================\n\nStarting Example\n\n===========================================")

# initialize the Bluetooth Core
core = BluenetBle()
core.setSettings("adminKeyForCrown", "memberKeyForHome", "guestKeyForOther")

print("Searching for Crownstones in range")
address = "d0:64:fd:10:54:f9"

core.connect(address)
core.control.setSwitchState(1)
core.control.disconnect()

core.shutDown()

print("===========================================\n\nFinished Example\n\n===========================================")

