from BluenetLib.lib.packets.CrownstoneErrors import CrownstoneErrors
from BluenetLib.lib.packets.seriviceDataParsers.parsers import parseOpCode3, parseOpCode4
from BluenetLib.lib.util.Conversion import Conversion
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
    uniqueIdentifier = 0
    
    validData = False
    
    def __init__(self, data):
        self.data = data
        self.parse()

    def parse(self):
        if len(self.data) == 17:
            self.opCode = self.data[0]
            if self.opCode == 3:
                parseOpCode3(self, self.data)
            elif self.opCode == 4:
                parseOpCode4(self, self.data)
            else:
                parseOpCode3(self, self.data)
        else:
            self.validData = False

    def isInSetupMode(self):
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
        returnDict["errorMode"]                 = self.errorMode
        returnDict["errors"]                    = errorsDictionary
    
        returnDict["uniqueElement"] =  self.uniqueIdentifier
        returnDict["timeIsSet"] =  self.timeIsSet
    
        return returnDict
    
    def decrypt(self, keyHexString):
        if len(self.data) == 17:
            encryptedArray = []
            self.opCode = self.data[0]
            
            for i in range(1, len(self.data)):
                encryptedArray.append(self.data[i])
            
            result = EncryptionHandler.decryptECB(encryptedArray, keyHexString)
            
            self.data = []
            self.data.append(self.opCode)
            
            self.data += result
            
            self.parse()
        else:
            print("Invalid data length")