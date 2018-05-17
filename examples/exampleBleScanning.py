#!/usr/bin/env python

"""An example that switches a Crownstone, and prints the power usage of all Crownstones."""

#!/usr/bin/env python
import time

from BluenetLib.BLE import BluenetBle

# initialize the Bluetooth Core
core = BluenetBle()
core.setSettings("adminKeyForCrown", "memberKeyForHome", "guestKeyForOther")

core.startScanning(3)

core.shutDown()