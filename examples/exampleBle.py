#!/usr/bin/env python

"""An example that switches a Crownstone, and prints the power usage of all Crownstones."""

print("\n\n\nStarting Example")

from BluenetLib import Bluenet

# Create new instance of Bluenet
from BluenetLib.lib.core.BluetoothCore import BluetoothCore

bluenet = Bluenet()

core = BluetoothCore()

core.startScanning()


print("\n\n\nFinished Example")