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
        
    def test_switchPacketHexKey(self):
        rawData = [0, 0, 100, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        key = Conversion.ascii_or_hex_string_to_16_byte_array("9e34c5a7da5c2b8d36e9fc5cf7497a6b")
        expectedKey = [158, 52, 197, 167, 218, 92, 43, 141, 54, 233, 252, 92, 247, 73, 122, 107]
        
        self.assertEqual(key, bytes(expectedKey))

        encryptionData = EncryptionHandler.encryptECB(rawData, key)
        
        encryptedDataExpected = [115, 162, 142, 55, 70, 208, 171, 55, 225, 152, 108, 53, 144, 169, 172, 179]

        decryptedData = EncryptionHandler.decryptECB(encryptionData, key)
        
        self.assertEqual(encryptionData, bytes(encryptedDataExpected))
        self.assertEqual(decryptedData, bytes(rawData))



if __name__ == '__main__':
    unittest.main()