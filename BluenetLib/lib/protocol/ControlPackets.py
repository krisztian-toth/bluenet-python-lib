from BluenetLib.lib.protocol.BlePackets import ControlPacket, FactoryResetPacket, keepAliveStatePacket
from BluenetLib.lib.protocol.BluenetTypes import ControlType

from BluenetLib.lib.util.Conversion import Conversion


class ControlPacketsGenerator:

	@staticmethod
	def getFactoryResetPacket():
		return Conversion.uint32_to_uint8_array(0xdeadbeef)


	@staticmethod
	def getSetSchedulePacket(data):
		return ControlPacket(ControlType.SCHEDULE_ENTRY).loadByteArray(data).getPacket()


	@staticmethod
	def getScheduleRemovePacket(timerIndex):
		return ControlPacket(ControlType.SCHEDULE_REMOVE).loadUInt8(timerIndex).getPacket()

	@staticmethod
	def getCommandFactoryResetPacket():
		return FactoryResetPacket().getPacket()

	@staticmethod
	def getSwitchStatePacket(switchState):
		"""
		:param switchState: number [0..1]
		"""

		convertedSwitchState = int(min(1,max(0,switchState))*100)

		return ControlPacket(ControlType.SWITCH).loadUInt8(convertedSwitchState).getPacket()

	@staticmethod
	def getResetPacket():
		return ControlPacket(ControlType.RESET).getPacket()

	@staticmethod
	def getPutInDFUPacket():
		return ControlPacket(ControlType.GOTO_DFU).getPacket()

	@staticmethod
	def getDisconnectPacket():
		return ControlPacket(ControlType.DISCONNECT).getPacket()

	@staticmethod
	def getRelaySwitchPacket(state):
		"""
		:param state: 0 or 1
		"""
		return ControlPacket(ControlType.RELAY).loadUInt8(state).getPacket()

	@staticmethod
	def getPwmSwitchPacket(switchState):
		"""
		:param state: number [0..1]
		:return:
		"""
		convertedSwitchState = int(min(1, max(0, switchState)) * 100)

		return ControlPacket(ControlType.PWM).loadUInt8(convertedSwitchState).getPacket()

	@staticmethod
	def getKeepAliveStatePacket(changeState, switchState, timeout):
		"""
		:param changeState:
		:param switchState:
		:param timeout:
		"""
		convertedSwitchState = int(min(1, max(0, switchState)) * 100)

		actionState = 0
		if changeState:
			actionState = 1

		return keepAliveStatePacket(actionState, convertedSwitchState, timeout).getPacket()

	@staticmethod
	def getKeepAliveRepeatPacket():
		return ControlPacket(ControlType.KEEP_ALIVE_REPEAT).getPacket()

	@staticmethod
	def getResetErrorPacket(errorMask):
		return ControlPacket(ControlType.RESET_ERRORS).loadUInt32(errorMask).getPacket()

	@staticmethod
	def getSetTimePacket(time):
		"""
		This is a LOCAL timestamp since epoch in seconds

		so if you live in GMT + 1 add 3600 to the timestamp
		:param time:
		:return:
		"""
		return ControlPacket(ControlType.SET_TIME).loadUInt32(time).getPacket()

	@staticmethod
	def getAllowDimmingPacket(allow):
		"""

		:param allow: bool
		:return:
		"""

		allowByte = 0
		if allow:
			allowByte = 1

		return ControlPacket(ControlType.ALLOW_DIMMING).loadUInt8(allowByte).getPacket()

	@staticmethod
	def getLockSwitchPacket(lock):
		"""
		:param lock: bool
		:return:
		"""

		lockByte = 0
		if lock:
			lockByte = 1

		return ControlPacket(ControlType.LOCK_SWITCH).loadUInt8(lockByte).getPacket()
