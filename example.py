#!/usr/bin/env python

"""An example that switches a Crownstone, and prints the power usage of all Crownstones."""

import time

from BluenetLib import Bluenet

# Function that's called when the power usage is updated.
def showPowerUsage(data):
	print("PowerUsage for Crownstone ID", data["crownstoneId"], "is", data["powerUsage"], "W")

# Create new instance of Bluenet
bluenet = Bluenet()

# Start up the USB bridge
bluenet.initializeUsbBridge("/dev/ttyUSB0")

# Set up event listeners
eventBus = bluenet.getEventBus()
topics   = bluenet.getTopics()
eventBus.subscribe(topics.powerUsageUpdate, showPowerUsage)

# This is the id of the Crownstone we will be switching
targetCrownstoneId = 1

# Switch this Crownstone on and off.
switchState = True
while (bluenet.isRunning):

	if switchState:
		print("Switching Crownstone on  (iteration: ", i,")")
	else:
		print("Switching Crownstone off (iteration: ", i,")")
	bluenet.switchCrownstone(targetCrownstoneId, on = switchState)

	switchState = not switchState
	time.sleep(2)
