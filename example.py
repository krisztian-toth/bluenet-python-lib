import time
from lib.core.Bluenet import Bluenet

def showPowerUsage(data):
	print("PowerUsage for CrownstoneId:", data[0], " is", data[1], "W")

# create new instance of Bluenet
bluenet = Bluenet()

# start up the USB bridge
bluenet.initializeUsbBridge("/dev/tty.SLAB_USBtoUART")

#set up event listeners
events = bluenet.getEventBus()
topics = bluenet.getTopics()
events.on(topics.powerUsageUpdate,  showPowerUsage )

time.sleep(2)

targetCrownstoneId = 235

print("Switching 235 on")
bluenet.switchCrownstone(targetCrownstoneId, 1)

time.sleep(2)
print("Switching 235 off")
bluenet.switchCrownstone(targetCrownstoneId, 0)

time.sleep(2)
print("Switching 235 on")
bluenet.switchCrownstone(targetCrownstoneId, 1)

time.sleep(2)
print("Switching 235 off")
bluenet.switchCrownstone(targetCrownstoneId, 0)
