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
bluenet.initializeUsbBridge("/dev/tty.usbmodemFA1331")

# Set up event listeners
myEventBus = bluenet.getEventBus()
myTopics   = bluenet.getTopics()
myEventBus.subscribe(myTopics.powerUsageUpdate, showPowerUsage)

# This is the id of the Crownstone we will be switching
targetCrownstoneId = 1

# Switch this Crownstone on and off.
switchState = True
for i in range(0,100):
	if not bluenet.isRunning:
		break

	if switchState:
		print("Switching Crownstone on  (iteration: ", i,")")
	else:
		print("Switching Crownstone off (iteration: ", i,")")
	bluenet.switchCrownstone(targetCrownstoneId, on = switchState)

	switchState = not switchState
	time.sleep(2)
