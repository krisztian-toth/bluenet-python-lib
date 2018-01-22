import unittest

from lib.protocol.ControlPackets import ControlPacketsGenerator


class TestControlPackets(unittest.TestCase):

	def setup(self):
		pass
	def tearDown(self):
		pass


	def test_getFactoryResetPacket(self):
		self.assertEqual(ControlPacketsGenerator.getFactoryResetPacket(), [239, 190, 173, 222])


	def test_createSetSchedulePacket(self):
		pass # TODO: implement


	def test_getSetSchedulePacket(self):
		self.assertEqual(ControlPacketsGenerator.getSetSchedulePacket([1,2,3]), [15, 0, 3, 0, 1, 2, 3])


	def test_getScheduleRemovePacket(self):
		self.assertEqual(ControlPacketsGenerator.getScheduleRemovePacket(2), [26, 0, 1, 0, 2])


	def test_getCommandFactoryResetPacket(self):
		self.assertEqual(ControlPacketsGenerator.getCommandFactoryResetPacket(), [5, 0, 4, 0, 239, 190, 173, 222])


	def test_getSwitchStatePacket(self):
		self.assertEqual(ControlPacketsGenerator.getSwitchStatePacket(0.0),  [0, 0, 1, 0, 0])
		self.assertEqual(ControlPacketsGenerator.getSwitchStatePacket(1),    [0, 0, 1, 0, 100])
		self.assertEqual(ControlPacketsGenerator.getSwitchStatePacket(0.99), [0, 0, 1, 0, 99])
		self.assertEqual(ControlPacketsGenerator.getSwitchStatePacket(0.4),  [0, 0, 1, 0, 40])


	def test_getResetPacket(self):
		self.assertEqual(ControlPacketsGenerator.getResetPacket(), [4, 0, 0, 0])


	def test_getPutInDFUPacket(self):
		self.assertEqual(ControlPacketsGenerator.getPutInDFUPacket(), [3, 0, 0, 0])


	def test_getDisconnectPacket(self):
		self.assertEqual(ControlPacketsGenerator.getDisconnectPacket(), [19, 0, 0, 0])


	def test_getRelaySwitchPacket(self):
		self.assertEqual(ControlPacketsGenerator.getRelaySwitchPacket(0), [16, 0, 1, 0, 0])
		self.assertEqual(ControlPacketsGenerator.getRelaySwitchPacket(1), [16, 0, 1, 0, 1])


	def test_getPwmSwitchPacket(self):
		self.assertEqual(ControlPacketsGenerator.getPwmSwitchPacket(0),    [1, 0, 1, 0, 0])
		self.assertEqual(ControlPacketsGenerator.getPwmSwitchPacket(0.33), [1, 0, 1, 0, 33])
		self.assertEqual(ControlPacketsGenerator.getPwmSwitchPacket(0.66), [1, 0, 1, 0, 66])
		self.assertEqual(ControlPacketsGenerator.getPwmSwitchPacket(1),    [1, 0, 1, 0, 100])


	def test_getKeepAliveStatePacket(self):
		self.assertEqual(ControlPacketsGenerator.getKeepAliveStatePacket(False, 1, 135), [6, 0, 4, 0, 0, 100, 135, 0])
		self.assertEqual(ControlPacketsGenerator.getKeepAliveStatePacket(True,  1, 0),   [6, 0, 4, 0, 1, 100, 0,   0])
		self.assertEqual(ControlPacketsGenerator.getKeepAliveStatePacket(True,  0, 500), [6, 0, 4, 0, 1, 0,   244, 1])


	def test_getKeepAliveRepeatPacket(self):
		self.assertEqual(ControlPacketsGenerator.getKeepAliveRepeatPacket(), [7,0,0,0])


	def test_getResetErrorPacket(self):
		self.assertEqual(ControlPacketsGenerator.getResetErrorPacket(0xabcdef02), [23, 0, 4, 0, 2, 239, 205, 171])


	def test_getSetTimePacket(self):
		self.assertEqual(ControlPacketsGenerator.getSetTimePacket(1516616561), [2, 0, 4, 0, 113, 187, 101, 90])


	def test_getAllowDimmingPacket(self):
		self.assertEqual(ControlPacketsGenerator.getAllowDimmingPacket(True),  [29, 0, 1, 0, 1])
		self.assertEqual(ControlPacketsGenerator.getAllowDimmingPacket(False), [29, 0, 1, 0, 0])

	def test_getLockSwitchPacket(self):
		self.assertEqual(ControlPacketsGenerator.getLockSwitchPacket(True),  [30, 0, 1, 0, 1])
		self.assertEqual(ControlPacketsGenerator.getLockSwitchPacket(False), [30, 0, 1, 0, 0])


if __name__ == '__main__':
    unittest.main()