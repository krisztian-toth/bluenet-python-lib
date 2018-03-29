from BluenetLib.lib.packets.seriviceDataParsers.opCode3.opCode3_type0 import parseOpcode3_type0

def parseOpcode3_type2(serviceData, data):
    if len(data) == 17:
        parseOpcode3_type0(serviceData, data)
    
        # apply differences between type 0 and type 2
        serviceData.stateOfExternalCrownstone = True
