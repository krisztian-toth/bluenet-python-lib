import unittest

from BluenetLib.lib.util.Conversion import Conversion
from BluenetLib.lib.util.Timestamp import reconstructTimestamp


class TestServiceDataParsingConversion(unittest.TestCase):

	def setup(self):
		pass
	def tearDown(self):
		pass


	def test_parseBitmask(self):
		bitArray = Conversion.uint32_to_bit_array(16)
		
		overCurrent = bitArray[31 - 0]
		overCurrentDimmer = bitArray[31 - 1]
		temperatureChip = bitArray[31 - 2]
		temperatureDimmer = bitArray[31 - 3]
		dimmerOnFailure = bitArray[31 - 4]
		dimmerOffFailure = bitArray[31 - 5]

		self.assertEqual(overCurrent, False)
		self.assertEqual(overCurrentDimmer, False)
		self.assertEqual(temperatureChip, False)
		self.assertEqual(temperatureDimmer, False)
		self.assertEqual(temperatureDimmer, False)
		self.assertEqual(dimmerOnFailure, True)
		self.assertEqual(dimmerOffFailure, False)
		



if __name__ == '__main__':
    unittest.main()