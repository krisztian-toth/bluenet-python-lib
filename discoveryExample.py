#!/usr/bin/env python

"""An example that prints all known Crownstone IDs."""

import time

from BluenetLib import Bluenet

# Create new instance of Bluenet
bluenet = Bluenet()

# Start up the USB bridge
bluenet.initializeUsbBridge("/dev/ttyUSB0")

# List the ids that have been seen
while (bluenet.isRunning):
	time.sleep(2)
	ids = bluenet.getCrownstoneIds()
	print("Crownstone IDs:", ids)

