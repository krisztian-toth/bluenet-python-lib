from lib.containerClasses.MeshStatePacket import MeshStatePacket
from lib.util.Conversion import Conversion
from lib.core.uart.UartTypes import RxOpcode
import time
import re

from lib.util.EventBus import eventBus, SystemTopics, Topics


class UartParser:
	def __init__(self):
		eventBus.subscribe(SystemTopics.uartNewPackage, self.parse)

	def parse(self, dataPacket):

		opCode = dataPacket.opCode

		if opCode >= RxOpcode.MESH_STATE_0 and opCode <= RxOpcode.MESH_STATE_LAST:
		# if opCode is 100 or opCode is 101:
		# if opCode is RxOpcode.MESH_STATE_0 or opCode is RxOpcode.MESH_STATE_1:
			extractor = MeshStatePacket(dataPacket.payload)
			extractor.broadcastState()
		elif opCode == int(RxOpcode.POWER_LOG_CURRENT):
			eventBus.emit(Topics.currentSamples, dataPacket.payload)
			# print("current samples", len(dataPacket.payload), dataPacket.payload)
			pass
		else:
			print("Unknown OpCode", opCode)


