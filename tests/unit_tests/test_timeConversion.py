import unittest

from BluenetLib.lib.util import reconstructTimestamp


class TestTimeConversion(unittest.TestCase):

	def setup(self):
		pass
	def tearDown(self):
		pass


	def test_TimeConvert1(self):
		reconstructed = reconstructTimestamp(1516206007.7995, 34186)
		self.assertEqual(reconstructed, 1516209546.0)



if __name__ == '__main__':
    unittest.main()