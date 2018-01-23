import time
from lib.core.Bluenet import Bluenet

def showPowerUsage(data):
	print("PowerUsage for CrownstoneId:", data["crownstoneId"], " is", data["powerUsage"], "W")

# create new instance of Bluenet
bluenet = Bluenet()

# start up the USB bridge
bluenet.initializeUsbBridge("/dev/tty.SLAB_USBtoUART")

#set up event listeners
events = bluenet.getEventBus()
topics = bluenet.getTopics()
events.on(topics.powerUsageUpdate,  showPowerUsage)

# this is the id of the Crownstone we will be switching
targetCrownstoneId = 235

# switch this Crownstone 100 times on and off.
switchState = 1
for i in range(0,100):
	if bluenet.isRunning:
		time.sleep(2)
		bluenet.switchCrownstone(targetCrownstoneId, switchState)
		if switchState is 1:
			print("Switching Crownstone", switchState, "on  (", i,")")
			switchState = 0
		else:
			print("Switching Crownstone", switchState, "off (", i,")")
			switchState = 1
