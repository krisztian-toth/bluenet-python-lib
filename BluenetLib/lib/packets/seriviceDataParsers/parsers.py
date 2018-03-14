from BluenetLib.lib.packets.seriviceDataParsers.opCode3.opCode3_type0 import parseOpcode3_type0
from BluenetLib.lib.packets.seriviceDataParsers.opCode3.opCode3_type1 import parseOpcode3_type1
from BluenetLib.lib.packets.seriviceDataParsers.opCode3.opCode3_type2 import parseOpcode3_type2
from BluenetLib.lib.packets.seriviceDataParsers.opCode3.opCode3_type3 import parseOpcode3_type3

def parseOpCode3(serviceData, data):
    if len(data) == 17:
        serviceData.dataType = data[1]
        if serviceData.dataType == 0:
            parseOpcode3_type0(serviceData, data)
        elif serviceData.dataType == 1:
            parseOpcode3_type1(serviceData, data)
        elif serviceData.dataType == 2:
            parseOpcode3_type2(serviceData, data)
        elif serviceData.dataType == 3:
            parseOpcode3_type3(serviceData, data)
        else:
            parseOpcode3_type0(serviceData, data)





from BluenetLib.lib.packets.seriviceDataParsers.opCode4.opCode4_type0 import parseOpcode4_type0

def parseOpCode4(serviceData, data):
    if len(data) == 17:
        serviceData.dataType = data[1]
        serviceData.setupMode = True
        if serviceData.dataType == 0:
            parseOpcode4_type0(serviceData, data)
        else:
            parseOpcode4_type0(serviceData, data)
