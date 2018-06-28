#!/usr/bin/env python3

"""An example that prints all Crownstone IDs seen on the mesh."""

import time

from BluenetLib import Bluenet

# Create new instance of Bluenet
bluenet = Bluenet()

# Start up the USB bridge.
# Fill in the correct device, see the readme.
# For firmware versions below 2.1, add the parameter baudrate=38400
bluenet.initializeUSB("/dev/tty.SLAB_USBtoUART")

# List the ids that have been seen
print("Listening for Crownstones on the mesh, this might take a while.")
while bluenet.running:
	time.sleep(2)
	ids = bluenet.getCrownstoneIds()
	print("Crownstone IDs seen so far:", ids)

