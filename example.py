import time

from lib.core.Bluenet import Bluenet

def showPowerUsage(data):
	print("PowerUsage for CrownstoneId:", data[0], " is", data[1], "W")

def showSwitchState(data):
	print("SwitchState for CrownstoneId:", data[0], " is", data[1])

# create new instance of Bluenet
bluenet = Bluenet()

# start up the USB bridge
bluenet.initializeUsbBridge()

#set up event listeners
events = bluenet.getEventBus()
topics = bluenet.getTopics()
events.on(topics.powerUsageUpdate,  showPowerUsage )
events.on(topics.switchStateUpdate, showSwitchState)

time.sleep(2)
bluenet.switchCrownstone(232, 1)

time.sleep(4)
bluenet.switchCrownstone(232, 0)