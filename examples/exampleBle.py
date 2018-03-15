#!/usr/bin/env python

"""An example that switches a Crownstone, and prints the power usage of all Crownstones."""

print("\n\n\nStarting Example")

from BluenetLib import Bluenet

# Create new instance of Bluenet
from BluenetLib.lib.core.BluetoothCore import BluetoothCore

bluenet = Bluenet()

core = BluetoothCore()
core.setSettings(True, "f40a7ab9eb1c9909a35e4b5bb1c07bcd", "dcad9f07f4a13339db066b4acf437646", "9332b7abf19b86f548156d88c687def6", "test")
core.connect("f2:6d:08:1c:a9:0c")
core.control.disconnect()


print("\n\n\nFinished Example")