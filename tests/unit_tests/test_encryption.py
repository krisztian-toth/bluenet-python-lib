import unittest

from BluenetLib.lib.util.Conversion import Conversion
from BluenetLib.lib.util.EncryptionHandler import EncryptionHandler


class TestEncryption(unittest.TestCase):

    def setup(self):
        pass
    def tearDown(self):
        pass


    def test_switchPacket(self):
        rawData = [0, 0, 1, 0, 100]
        sessionNonce = Conversion.string_to_uint8_array("12345")
        encryptionData = EncryptionHandler.encryptCTR(rawData, [128,128,128], sessionNonce, Conversion.string_to_uint8_array("AdminKeyOf16Byte"))
        self.assertEqual(encryptionData, bytes([171,199,94,51,230,26,253,144,182,105,56,210,94,165,184,243]))



if __name__ == '__main__':
    unittest.main()