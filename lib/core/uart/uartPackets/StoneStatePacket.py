import time

from lib.util.Conversion import Conversion
from lib.util.EventBus   import eventBus, SystemTopics
from lib.util.Timestamp  import reconstructTimestamp

STONE_STATE_PACKET_SIZE = 14

class StoneStatePacket:
	type = 0

	crownstoneId = 0
	switchState = 0
	flagBitMask = 0
	temperature = 0
	powerFactor = 0
	powerUsageReal = 0
	powerUsageApparent = 0
	energyUsed = 0
	partialTimestamp = 0
	timestamp = 0

	deprecated = False

	def __init__(self, meshStateItem):
		if len(meshStateItem) != STONE_STATE_PACKET_SIZE:
			print("ERROR: Invalid length of StoneStatePacket", len(meshStateItem), meshStateItem)

		self.type = meshStateItem[0]

		if self.type is 0 or self.type is 2:
			self.parseState(meshStateItem[1:])
		else:
			print("Got error payload. Ignoring for now")


	def parseState(self, meshStateItemState):
		self.crownstoneId 		= meshStateItemState[0]
		self.switchState    	= meshStateItemState[1]
		self.flagBitMask 		= meshStateItemState[2]
		self.temperature 		= meshStateItemState[3]
		self.powerFactor 		= float(meshStateItemState[4]) / 127
		self.powerUsageReal 	= float(Conversion.uint8_array_to_uint16(meshStateItemState[5:7])) / 8
		self.powerUsageApparent = self.powerUsageReal / self.powerFactor
		self.energyUsed 		= Conversion.uint8_array_to_int32(meshStateItemState[7:11])
		self.partialTimestamp 	= Conversion.uint8_array_to_uint16(meshStateItemState[11:13])
		self.timestamp 			= reconstructTimestamp(time.time(), self.partialTimestamp)

		if self.crownstoneId == 0:
			self.deprecated = True

	def constuctTimestamp(self):
		pass

	def broadcastState(self):
		if self.deprecated:
			return

		# tell the system this advertisement.
		eventBus.emit(SystemTopics.stateUpdate, (self.crownstoneId, self))

	def getDict(self):
		dict = {}

		dict["crownstoneId"] 	   = self.crownstoneId
		dict["switchState"] 	   = self.switchState
		dict["flagBitMask"] 	   = self.flagBitMask
		dict["temperature"] 	   = self.temperature
		dict["powerFactor"] 	   = self.powerFactor
		dict["powerUsageReal"] 	   = self.powerUsageReal
		dict["powerUsageApparent"] = self.powerUsageApparent
		dict["energyUsed"] 		   = self.energyUsed
		dict["timestamp"] 		   = self.timestamp

		return dict