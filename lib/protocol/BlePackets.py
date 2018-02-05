from lib.protocol.BluenetTypes import ControlType, OpCode
from lib.util.Conversion import Conversion


class BLEPacket:
    type = 0
    lengthAsUint8Array = [0,0]
    payload = []

    def __init__(self, packetType):
        self.type = packetType

    def loadString(self, string):
        self.payload = Conversion.string_to_uint8_array(string)
        return self._process()

    def loadInteger(self, integer):
        self.payload = [Conversion.int8_to_uint8(integer)]
        return self._process()

    def loadUInt8(self, uint8):
        self.payload = [uint8]
        return self._process()

    def loadUInt16(self, uint16):
        self.payload = Conversion.uint16_to_uint8_array(uint16)
        return self._process()

    def loadUInt32(self, uint32):
        self.payload = Conversion.uint32_to_uint8_array(uint32)
        return self._process()

    def loadByteArray(self, byteArray):
        self.payload = byteArray
        return self._process()


    def _process(self):
        self.lengthAsUint8Array = Conversion.uint16_to_uint8_array(len(self.payload))
        return self

    def getPacket(self):
        packet = []
        packet.append(self.type)
        packet.append(0)          # reserved
        packet += self.lengthAsUint8Array
        packet += self.payload

        return packet

class ControlPacket(BLEPacket):

    def __init__(self, packetType):
        super().__init__(packetType)


    def getPacket(self):
        packet = []
        packet.append(self.type)
        packet.append(0)
        packet += self.lengthAsUint8Array
        packet += self.payload

        return packet



class keepAliveStatePacket(ControlPacket):
    def __init__(self, action, state, timeout):
        packet = []
        packet.append(action)
        packet.append(state)
        timeoutByteArray = Conversion.uint16_to_uint8_array(timeout)
        packet += timeoutByteArray

        super().__init__(ControlType.KEEP_ALIVE_STATE)
        self.loadByteArray(packet)




class FactoryResetPacket(ControlPacket):

    def __init__(self):
        super().__init__(ControlType.FACTORY_RESET)
        self.loadUInt32(0xdeadbeef)



class ReadConfigPacket(BLEPacket):
    def getOpCode(self):
        return OpCode.READ

    def getPacket(self):
        packet = []
        packet.append(self.type)
        packet.append(self.getOpcode())
        packet += self.lengthAsUint8Array
        packet += self.payload
        return packet

class WriteConfigPacket(ReadConfigPacket):
    def getOpCode(self):
        return OpCode.WRITE





class ReadStatePacket(BLEPacket):
    def getOpCode(self):
        return OpCode.READ

    def getPacket(self):
        packet = []
        packet.append(self.type)
        packet.append(self.getOpcode())
        packet += self.lengthAsUint8Array
        packet += self.payload
        return packet


class WriteStatePacket(ReadStatePacket):
    def getOpCode(self):
        return OpCode.WRITE


class NotificationStatePacket(ReadStatePacket):
    def __init__(self, packetType, subscribe):
        super().__init__(packetType)
        if subscribe:
            self.loadUInt8(1)
        else:
            self.loadUInt8(0)

    def getOpCode(self):
        return OpCode.NOTIFY


