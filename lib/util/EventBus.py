import uuid
from enum import Enum



class SystemTopics(Enum):
	uartNewPackage 	= 'uartNewPackage' # used for Ready Packets. This comes from the UartReadBuffer and data is a UartPacket.
	uartWriteData 	= 'uartWriteData'  # used to write to the UART. Data is array of bytes.
	cleanUp 		= 'cleanUp'		   # used to propagate CTRL+C throughout the modules.


class Topics(Enum):
	powerUsageUpdate  = "powerUsageReal" # tuple of (crownstoneId, powerUsage)
	switchStateUpdate = "switchState"	 # tuple of (crownstoneId, switchState)





class EventBus:
	topics = {}
	subscriberIds = {}

	def __init__(self):
		pass

	def on(self, topic, callback):
		print("subscribing", topic)
		if topic not in self.topics:
			self.topics[topic] = {}

		subscriptionId = str(uuid.uuid4())
		self.subscriberIds[subscriptionId] = topic
		self.topics[topic][subscriptionId] = callback

		return subscriptionId

	def emit(self, topic, data = True):
		if topic in self.topics:
			for subscriptionId in self.topics[topic]:
				self.topics[topic][subscriptionId](data)


	def off(self, subscriptionId):
		if subscriptionId in self.subscriberIds:
			topic = self.subscriberIds[subscriptionId]
			if topic in self.topics:
				self.topics[topic].pop(subscriptionId)

			self.subscriberIds.pop(subscriptionId)
		else:
			print("Subscription ID cannot be found.")


eventBus = EventBus()
