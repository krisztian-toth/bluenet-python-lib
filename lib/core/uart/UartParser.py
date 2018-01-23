from lib.containerClasses.MeshStatePacket import MeshStatePacket
from lib.util.Conversion import Conversion
import time
import re

from lib.util.EventBus import eventBus, SystemTopics


class UartParser:
	def __init__(self):
		eventBus.on(SystemTopics.uartNewPackage, self.parse)

	def parse(self, dataPacket):

		opCode = dataPacket.opCode

		if opCode is 100 or opCode is 101:
			extractor = MeshStatePacket(dataPacket.payload)
			extractor.broadcastState()
		else:
			print("Unknown OpCode", opCode)


