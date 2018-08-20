import unittest

from BluenetLib import Util
from BluenetLib.lib.util.Conversion import Conversion


class TestAccessAddress(unittest.TestCase):

	def setup(self):
		pass
	def tearDown(self):
		pass

	def test_validateAccessAddress(self):
		self.assertEqual(Util.validateMeshAccessAddress(Conversion.uint32_to_uint8_array(2198409685)), False)
		



if __name__ == '__main__':
	unittest.main()