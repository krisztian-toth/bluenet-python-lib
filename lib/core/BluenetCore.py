from lib.core.uart.UartBridge import UartBridge
from lib.core.uart.UartWrapper import UartWrapper
from lib.dataFlowManagers.StoneStateManager import StoneStateManager
from lib.protocol.BlePackets import ControlPacket
from lib.protocol.BluenetTypes import IntentType, MeshMultiSwitchType, ControlType
from lib.protocol.MeshPackets import StoneMultiSwitchPacket, MeshMultiSwitchPacket
from lib.util.EventBus import SystemTopics, eventBus, Topics

import signal # used to catch control C

class BluenetCore:
	uartBridge = None
	stoneStateManager = None
	isRunning = True

	def __init__(self):
		self.stoneStateManager = StoneStateManager()

	def initializeUsbBridge(self, port, catchSIGINT = True):
		# listen for CTRL+C and handle the exit cleanly.
		if catchSIGINT:
			signal.signal(signal.SIGINT, self.__stopAll)

		baudrate = 38400

		# init the uart bridge
		self.uartBridge = UartBridge(port, baudrate)
		self.uartBridge.start()


	def __stopAll(self, source, frame):
		self.stop()


	def stop(self):
		print("Quitting BluenetLib...")
		self.uartBridge.stop()
		self.isRunning = False


	def switchCrownstone(self, crownstoneId, on):
		"""
		:param crownstoneId:
		:param on:  Boolean
		:return:
		"""
		state = 1
		if not on:
			state = 0

		self.__switchCrownstone(crownstoneId, state)


	def dimCrownstone(self, crownstoneId, value):
		# dimming is used when the value is [0 .. 99], 100 is turning on the relay. We map 0..1 to 0..0.99
		value = min(0.99, max(0,value) * 0.99)

		self.__switchCrownstone(crownstoneId, value)


	def getEventBus(self):
		return eventBus


	def getTopics(self):
		return Topics


	def getCrownstoneIds(self):
		return self.stoneStateManager.getIds()

	def isRunning(self):
		return self.isRunning

	def getLatestCrownstoneData(self, crownstoneId):
		self.stoneStateManager.getLatestCrownstoneData(crownstoneId)

	# MARK: Private

	def __switchCrownstone(self, crownstoneId, value):
		"""
		:param crownstoneId:
		:param value: 0 .. 1
		:return:
		"""

		# forcibly map the input from [any .. any] to [0 .. 1]
		correctedValue = min(1,max(0,value))

		# create a stone switch state packet to go into the multi switch
		stoneSwitchPacket 		= StoneMultiSwitchPacket(crownstoneId, correctedValue, 0, IntentType.MANUAL)

		# wrap it in a mesh multiswitch packet
		meshMultiSwitchPacket 	= MeshMultiSwitchPacket(MeshMultiSwitchType.SIMPLE_LIST, [stoneSwitchPacket]).getPacket()

		# wrap that in a control packet
		controlPacket 			= ControlPacket(ControlType.MESH_MULTI_SWITCH).loadByteArray(meshMultiSwitchPacket).getPacket()

		# finally wrap it in an Uart packet
		uartPacket 				= UartWrapper(1, controlPacket).getPacket()

		# send over uart
		eventBus.emit(SystemTopics.uartWriteData, uartPacket)