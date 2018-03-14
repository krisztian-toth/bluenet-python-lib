import unittest

from BluenetLib.lib.core.uart.UartTypes import UartTxType
from BluenetLib.lib.util.Conversion import Conversion


class TestControlPackets(unittest.TestCase):

    def setup(self):
        pass
    def tearDown(self):
        pass


    def test_getFactoryResetPacket(self):
        self.assertEqual(Conversion.uint8_array_to_uint16([217,39]), UartTxType.POWER_LOG_VOLTAGE)



if __name__ == '__main__':
    unittest.main()