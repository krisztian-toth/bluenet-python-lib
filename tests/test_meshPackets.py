import unittest

from lib.protocol.BluenetTypes import MeshKeepAliveTypes, MeshCommandType, IntentType, MeshMultiSwitchType
from lib.protocol.MeshPackets import StoneKeepAlivePacket, MeshKeepAlivePacket, MeshCommandPacket, \
	StoneMultiSwitchPacket, MeshMultiSwitchPacket


class TestMeshPackets(unittest.TestCase):

	def setup(self):
		pass
	def tearDown(self):
		pass


	def test_StoneKeepAlivePacket(self):
		self.assertEqual(StoneKeepAlivePacket(1, True, 0.2).getPacket(), [1,20])

	def test_MeshKeepAlivePacket(self):
		skaPackets = []
		for i in range(0,3):
			skaPackets.append(StoneKeepAlivePacket(i+1, True, 0.2))


		self.assertEqual(MeshKeepAlivePacket(MeshKeepAliveTypes.SHARED_TIMEOUT, 60, skaPackets).getPacket(), [0, 60, 0, 3, 1, 20, 2, 20, 3, 20])


	def test_MeshCommandPacket(self):
		self.assertEqual(MeshCommandPacket(MeshCommandType.CONTROL, [1,2,3,4], [0xFF, 0xFF]).getPacket(), [0, 0, 4, 1, 2, 3, 4, 255, 255])


	def test_StoneMultiSwitchPacket(self):
		self.assertEqual(StoneMultiSwitchPacket(1,0.5,15,IntentType.REGION_EXIT).getPacket(), [1, 50, 15, 0, 1])


	def test_MeshMultiSwitchPacket(self):
		smsPackets = []
		for i in range(0, 3):
			smsPackets.append(StoneMultiSwitchPacket(i+1,0.5,15,IntentType.REGION_EXIT))

		self.assertEqual(MeshMultiSwitchPacket(MeshMultiSwitchType.SIMPLE_LIST, smsPackets).getPacket(), [0, 3, 1, 50, 15, 0, 1, 2, 50, 15, 0, 1, 3, 50, 15, 0, 1])


if __name__ == '__main__':
    unittest.main()