import time

from BluenetLib import Bluenet

def showPowerUsage(data):
	print("PowerUsage for CrownstoneId:", data["crownstoneId"], " is", data["powerUsage"], "W")

# create new instance of Bluenet
bluenet = Bluenet()

# start up the USB bridge
bluenet.initializeUsbBridge("/dev/tty.SLAB_USBtoUART")

#set up event listeners
events = bluenet.getEventBus()
topics = bluenet.getTopics()
events.subscribe(topics.powerUsageUpdate, showPowerUsage)

# this is the id of the Crownstone we will be switching
targetCrownstoneId = 235

# switch this Crownstone 100 times on and off.
switchState = True
for i in range(0,100):
	if bluenet.isRunning:
		time.sleep(2)
		bluenet.switchCrownstone(targetCrownstoneId, on = switchState)
		if switchState:
			print("Switching Crownstone", switchState, "on  (iteration: ", i,")")
		else:
			print("Switching Crownstone", switchState, "off (iteration: ", i,")")

		switchState = not switchState