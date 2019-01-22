from BluenetLib.lib.packets.CrownstoneErrors import CrownstoneErrors
from BluenetLib.lib.packets.seriviceDataParsers.parsers import parseOpCode3, parseOpCode4, parseOpCode5, parseOpCode6
from BluenetLib.lib.protocol.BluenetTypes import DeviceType
from BluenetLib.lib.util.EncryptionHandler import EncryptionHandler


class ServiceData:
    
    def __init__(self, data):
        self.opCode = 0
        self.dataType = 0
        self.crownstoneId = 0
        self.switchState = 0
        self.flagsBitmask = 0
        self.temperature = 0
        self.powerFactor = 1
        self.powerUsageReal = 0
        self.powerUsageApparent = 0
        self.accumulatedEnergy = 0
        self.setupMode = False
        self.stateOfExternalCrownstone = False
        self.data = None
        self.dataString = ""
        self.dimmingAvailable = False
        self.dimmingAllowed = False
        self.hasError = False
        self.switchLocked = False
        self.partialTimestamp = 0
        self.timestamp = -1
        self.validation = 0x00  # Will be 0xFAif it is set.
   
        self.errorTimestamp = 0
        self.errorsBitmask = 0
        self.errorMode = False
        self.timeIsSet = False
        self.switchCraftEnabled = False
        self.uniqueIdentifier = 0
   
        self.validData = False
        self.dataReadyForUse = False  # decryption is successful if this is true
    
        self.deviceType = DeviceType.UNDEFINED
        self.rssiOfExternalCrownstone = 0
 
        self.encryptedData = []
        self.encryptedDataStartIndex = 0
        
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
        if not self.validData:
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

        returnDict["rssiOfExternalCrownstone"]  = self.rssiOfExternalCrownstone
    
        return returnDict
    
    
    def getSummary(self):
        errorsDictionary = CrownstoneErrors(self.errorsBitmask).getDictionary()
    
        returnDict = {}
    
        returnDict["id"] = self.crownstoneId
        returnDict["setupMode"] = self.isInSetupMode()
        returnDict["switchState"] = self.switchState
        returnDict["temperature"] = self.temperature
        returnDict["powerFactor"] = self.powerFactor
        returnDict["powerUsageReal"] = self.powerUsageReal
        returnDict["powerUsageApparent"] = self.powerUsageApparent
        returnDict["accumulatedEnergy"] = self.accumulatedEnergy
        returnDict["dimmingAvailable"] = self.dimmingAvailable
        returnDict["dimmingAllowed"] = self.dimmingAllowed
        returnDict["switchLocked"] = self.switchLocked
        returnDict["switchCraftEnabled"] = self.switchCraftEnabled
        returnDict["timeIsSet"] = self.timeIsSet
        returnDict["timestamp"] = self.timestamp
        returnDict["hasError"] = self.hasError
        returnDict["errorMode"] = self.errorMode
        returnDict["errors"] = errorsDictionary
    
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
            