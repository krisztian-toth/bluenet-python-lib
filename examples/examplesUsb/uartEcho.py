#!/usr/bin/env python3

"""An example that switches a Crownstone, and prints the power usage of all Crownstones."""

import time
from BluenetLib import Bluenet, BluenetEventBus, UsbTopics


# Create new instance of Bluenet
bluenet = Bluenet()

# Function that's called when the power usage is updated.
def showUartMessage(data):
	print("Received payload", data)

# Start up the USB bridge.
# Fill in the correct device, see the readme.
# For firmware versions below 2.1, add the parameter baudrate=38400
bluenet.initializeUSB("/dev/ttyUSB0")

# Set up event listeners
BluenetEventBus.subscribe(UsbTopics.uartMessage, showUartMessage)

bluenet.uartEcho("HelloWorld")
time.sleep(0.2)
bluenet.uartEcho("HelloWorld")
time.sleep(0.2)
bluenet.uartEcho("HelloWorld")
time.sleep(0.2)
bluenet.uartEcho("HelloWorld")
time.sleep(0.2)
bluenet.uartEcho("HelloWorld")
time.sleep(0.2)
bluenet.uartEcho("HelloWorld")
time.sleep(0.2)
bluenet.uartEcho("HelloWorld")
time.sleep(0.2)
bluenet.uartEcho("HelloWorld")
time.sleep(0.2)
bluenet.uartEcho("HelloWorld")
time.sleep(0.2)
bluenet.uartEcho("HelloWorld")
time.sleep(0.2)
bluenet.uartEcho("HelloWorld")
time.sleep(0.2)

bluenet.stop()