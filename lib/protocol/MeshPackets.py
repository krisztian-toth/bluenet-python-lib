from lib.util.Conversion import Conversion


class StoneKeepAlivePacket:
	crownstoneId = 0
	actionAndState = 0

	def __init__(self, crownstoneId, action, state):
		'''
		:param crownstoneId: byte
		:param action:  boolean
		:param state:  number [0..1]
		'''

		switchState = min(1, max(0, state)) * 100
		if not action:
			switchState = 255

		self.crownstoneId = crownstoneId
		self.actionAndState = switchState


	def getPacket(self):
		packet = []
		packet.append(self.crownstoneId)
		packet.append(self.actionAndState)
		return packet


class MeshKeepAlivePacket:
	type = 0
	timeout = 0
	reserved = []
	packets = []

	def __init__(self, packetType, timeout, packets):
		self.type = packetType
		self.timeout = timeout
		self.packets = packets
		self.reserved = [0,0]

	def getPacket(self):
		packet = []
		timeoutArray = Conversion.uint16_to_uint8_array(self.timeout)
		packet += timeoutArray
		packet.append(len(self.packets))
		for keepAlivePacket in self.packets:
			packet += keepAlivePacket.getPacket()
		return packet


class MeshCommandPacket:
	type = 0
	bitmask = 0
	crownstoneIds = []
	payload = []

	def __init__(self, packetType, crownstoneIds, payload):
		self.type = packetType
		self.crownstoneIds = crownstoneIds
		self.payload = payload

	def getPacket(self):
		packet = []
		packet.append(self.type)
		packet.append(self.bitmask)
		packet.append(len(self.crownstoneIds))
		packet += self.crownstoneIds
		packet += self.payload

		return packet


class StoneMultiSwitchPacket:
	timeout = 0
	crownstoneId = 0
	state = 0
	intent = 0

	def __init__(self, crownstoneId, state, timeout, intent):
		self.crownstoneId = crownstoneId
		self.state = state
		self.timeout = timeout
		self.intent = intent

	def getPacket(self):
		packet = []
		packet.append(self.crownstoneId)
		packet.append(self.state)
		packet += Conversion.uint16_to_uint8_array(self.timeout)
		packet.append(self.intent)

		return packet


class MeshMultiSwitchPacket:
	type = 0
	packets = []

	def __init__(self, packetType, packets):
		self.type = packetType
		self.packets = packets

	def getPacket(self):
		packet = []
		packet.append(self.type)
		packet.append(len(self.packets))
		for stonePacket in self.packets:
			packet += stonePacket.getPacket()

		return packet