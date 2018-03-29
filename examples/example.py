#!/usr/bin/env python

"""An example that switches a Crownstone, and prints the power usage of all Crownstones."""

import time
from BluenetLib import Bluenet, BluenetEventBus, Topics


# Function that's called when the power usage is updated.
def showPowerUsage(data):
	print("PowerUsage for Crownstone ID", data["id"], "is", data["powerUsage"], "W")

# Create new instance of Bluenet
bluenet = Bluenet()

# Start up the USB bridge
bluenet.initializeUSB("/dev/tty.SLAB_USBtoUART")

# Set up event listeners
BluenetEventBus.subscribe(Topics.powerUsageUpdate, showPowerUsage)

# This is the id of the Crownstone we will be switching
targetCrownstoneId = 10

# Switch this Crownstone on and off.
switchState = True
for i in range(0,100):
	if not bluenet.running:
		break

	if switchState:
		print("Switching Crownstone on  (iteration: ", i,")")
	else:
		print("Switching Crownstone off (iteration: ", i,")")
	bluenet.switchCrownstone(targetCrownstoneId, on = switchState)

	switchState = not switchState
	time.sleep(2)

