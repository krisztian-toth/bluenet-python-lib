#!/usr/bin/env python

"""An example that switches a Crownstone, and prints the power usage of all Crownstones."""

#!/usr/bin/env python
import time

from BluenetLib.BLE import BluenetBle
from BluenetLib import BluenetEventBus, Topics


# Function that's called when the power usage is updated.
def showData(data):
	print("data", data)


# Set up event listeners
BluenetEventBus.subscribe(Topics.advertisement, showData)

# initialize the Bluetooth Core
core = BluenetBle()
core.setSettings("adminKeyForCrown", "memberKeyForHome", "guestKeyForOther")

core.startScanning(10)

core.shutDown()