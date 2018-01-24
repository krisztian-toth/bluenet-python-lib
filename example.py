import time

from BluenetLib import Bluenet

def showPowerUsage(data):
	print("PowerUsage for CrownstoneId:", data["crownstoneId"], " is", data["powerUsage"], "W")

# create new instance of Bluenet
bluenet = Bluenet()

# start up the USB bridge
bluenet.initializeUsbBridge("/dev/tty.SLAB_USBtoUART")

#set up event listeners
eventBus = bluenet.getEventBus()
topics   = bluenet.getTopics()
eventBus.subscribe(topics.powerUsageUpdate, showPowerUsage)

# this is the id of the Crownstone we will be switching
targetCrownstoneId = 235

# switch this Crownstone 100 times on and off.
switchState = True
for i in range(0,100):
	if not bluenet.isRunning:
		break

	bluenet.switchCrownstone(targetCrownstoneId, on = switchState)
	if switchState:
		print("Switching Crownstone on  (iteration: ", i,")")
	else:
		print("Switching Crownstone off (iteration: ", i,")")

	switchState = not switchState
	time.sleep(2)