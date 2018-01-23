from lib.core.uart.UartBridge import UartBridge
from lib.core.uart.UartWrapper import UartWrapper
from lib.protocol.BlePackets import ControlPacket
from lib.protocol.BluenetTypes import IntentType, MeshMultiSwitchType, ControlType
from lib.protocol.MeshPackets import StoneMultiSwitchPacket, MeshMultiSwitchPacket
from lib.util.EventBus import SystemTopics, eventBus, Topics

import signal # used to catch control C

class Bluenet:
	uartBridge = None

	def __init__(self):
		pass


	def initializeUsbBridge(self, port):
		# listen for CTRL+C and handle the exit cleanly.
		signal.signal(signal.SIGINT, self.stopAll)
		baudrate = 38400

		# init the uart bridge
		self.uartBridge = UartBridge(port, baudrate)
		self.uartBridge.start()


	def stopAll(self, source, frame):
		print("Quitting Bluenet...")
		self.uartBridge.stop()


	def switchCrownstone(self, crownstoneId, value):
		"""
		:param crownstoneId:
		:param value: 0 .. 1
		:return:
		"""

		# create a stone switch state packet to go into the multi switch
		stoneSwitchPacket 		= StoneMultiSwitchPacket(crownstoneId, value, 0, IntentType.MANUAL)

		# wrap it in a mesh multiswitch packet
		meshMultiSwitchPacket 	= MeshMultiSwitchPacket(MeshMultiSwitchType.SIMPLE_LIST, [stoneSwitchPacket]).getPacket()

		# wrap that in a control packet
		controlPacket 			= ControlPacket(ControlType.MESH_MULTI_SWITCH).loadByteArray(meshMultiSwitchPacket).getPacket()

		# finally wrap it in an Uart packet
		uartPacket 				= UartWrapper(1, controlPacket).getPacket()

		# send over uart
		eventBus.emit(SystemTopics.uartWriteData, uartPacket)


	def dimCrownstone(self, crownstoneId, value):
		Bluenet.switchCrownstone(crownstoneId, value)


	def getEventBus(self):
		return eventBus

	def getTopics(self):
		return Topics

