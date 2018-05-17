from BluenetLib.lib.packets.CrownstoneErrors import CrownstoneErrors
from BluenetLib.lib.packets.seriviceDataParsers.parsers import parseOpCode3, parseOpCode4, parseOpCode5, parseOpCode6
from BluenetLib.lib.protocol.BluenetTypes import DeviceType
from BluenetLib.lib.util.EncryptionHandler import EncryptionHandler


class ServiceData:
    opCode = 0
    dataType = 0
    crownstoneId = 0
    switchState = 0
    flagsBitmask = 0
    temperature = 0
    powerFactor = 1
    powerUsageReal = 0
    powerUsageApparent = 0
    accumulatedEnergy = 0
    setupMode = False
    stateOfExternalCrownstone = False
    data = None
    dataString = ""
    dimmingAvailable = False
    dimmingAllowed = False
    hasError = False
    switchLocked = False
    partialTimestamp = 0
    timestamp = -1
    validation = 0x0000 # Will be 0xFACE if it is set.
    
    errorTimestamp = 0
    errorsBitmask = 0
    errorMode = False
    timeIsSet = False
    switchCraftEnabled = False
    uniqueIdentifier = 0
    
    validData = False
    dataReadyForUse = False # decryption is successful if this is true
    
    deviceType = DeviceType.UNDEFINED
    rssiOfExternalCrownstone = 0

    encryptedData = []
    encryptedDataStartIndex = 0
    
    def __init__(self, data):
        self.data = data
        self.parse()

    def parse(self):
        self.validData = True
        if len(self.data) == 18:
            self.opCode = self.data[0]
            self.encryptedData = self.data[2:]
            self.encryptedDataStartIndex = 2
            if self.opCode == 5:
                parseOpCode5(self, self.data)
            elif self.opCode == 6:
                parseOpCode6(self, self.data)
            else:
                parseOpCode5(self, self.data)
                
        elif len(self.data) == 17:
            self.opCode = self.data[0]
            self.encryptedData = self.data[1:]
            self.encryptedDataStartIndex = 1
            if self.opCode == 3:
                parseOpCode3(self, self.data)
            elif self.opCode == 4:
                parseOpCode4(self, self.data)
            else:
                parseOpCode3(self, self.data)
                
        else:
            self.validData = False

    def isInSetupMode(self):
        if self.validData:
            return False
    
        return self.setupMode
    
    
    def getDictionary(self):
        errorsDictionary = CrownstoneErrors(self.errorsBitmask).getDictionary()
        
        returnDict = {}
        
        returnDict["opCode"]                    = self.opCode
        returnDict["dataType"]                  = self.dataType
        returnDict["stateOfExternalCrownstone"] = self.stateOfExternalCrownstone
        returnDict["hasError"]                  = self.hasError
        returnDict["setupMode"]                 = self.isInSetupMode()
        returnDict["id"]                        = self.crownstoneId
        returnDict["switchState"]               = self.switchState
        returnDict["flagsBitmask"]              = self.flagsBitmask
        returnDict["temperature"]               = self.temperature
        returnDict["powerFactor"]               = self.powerFactor
        returnDict["powerUsageReal"]            = self.powerUsageReal
        returnDict["powerUsageApparent"]        = self.powerUsageApparent
        returnDict["accumulatedEnergy"]         = self.accumulatedEnergy
        returnDict["timestamp"]                 = self.timestamp
        returnDict["dimmingAvailable"]          = self.dimmingAvailable
        returnDict["dimmingAllowed"]            = self.dimmingAllowed
        returnDict["switchLocked"]              = self.switchLocked
        returnDict["switchCraftEnabled"]        = self.switchCraftEnabled
        returnDict["errorMode"]                 = self.errorMode
        returnDict["errors"]                    = errorsDictionary
    
        returnDict["uniqueElement"]             =  self.uniqueIdentifier
        returnDict["timeIsSet"]                 =  self.timeIsSet

        returnDict["deviceType"]                = self.deviceType
        returnDict["rssiOfExternalCrownstone"]  = self.rssiOfExternalCrownstone
    
        return returnDict
    
    def decrypt(self, keyHexString):
        if self.validData and len(self.encryptedData) == 16 and len(keyHexString) >= 16:
            result = EncryptionHandler.decryptECB(self.encryptedData, keyHexString)
            
            for i in range(0, len(self.encryptedData)):
                self.data[i+self.encryptedDataStartIndex] = result[i]
            
            self.parse()
            self.dataReadyForUse = True
        else:
            self.dataReadyForUse = False
            print("Invalid data length")