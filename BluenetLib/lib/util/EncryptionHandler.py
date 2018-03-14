import pyaes

from BluenetLib.lib.util.Conversion import Conversion


class EncryptionHandler:
    
    def __init__(self):
        pass
    
    @staticmethod
    def decryptECB(uint8Array, key):
        uint8ArrayKey = Conversion.hex_string_to_uint8_array(key)
        aes = pyaes.AESModeOfOperationECB(uint8ArrayKey)
        
        stringPayload = "".join(chr(b) for b in uint8Array)
        
        # Since there is no state stored in this mode of operation, it
        # is not necessary to create a new aes object for decryption.
        decrypted = aes.decrypt(stringPayload)
        
        return decrypted

    @staticmethod
    def encryptECB(data, key):
        pass

    @staticmethod
    def decryptCTR(data, key):
        pass

    @staticmethod
    def encryptCTR(data, key):
        pass