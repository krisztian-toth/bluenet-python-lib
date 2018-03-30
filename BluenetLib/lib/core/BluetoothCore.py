from BluenetLib.lib.core.modules.Gatherer import Gatherer
from BluenetLib.lib.util.JsonFileStore import JsonFileStore

from BluenetLib.Exceptions import BleError, BluenetError, BluenetBleException, BluenetException
from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.core.bluenet_modules.BleHandler import BleHandler
from BluenetLib.lib.core.bluenet_modules.ControlHandler import ControlHandler
from BluenetLib.lib.core.bluenet_modules.SetupHandler import SetupHandler
from BluenetLib.lib.core.bluenet_modules.StateHandler import StateHandler

from BluenetLib.lib.core.modules.BluenetSettings import BluenetSettings
from BluenetLib.lib.core.modules.NearestSelector import NearestSelector
from BluenetLib.lib.topics.SystemBleTopics import SystemBleTopics
from BluenetLib.lib.topics.Topics import Topics


class BluetoothCore:
    control = None
    setup   = None
    config  = None
    state   = None
    mesh    = None
    ble     = None
    
    def __init__(self, hciIndex=0):
        self.settings = BluenetSettings()
        self.control  = ControlHandler(self)
        self.setup    = SetupHandler(self)
        self.state    = StateHandler(self)
        self.ble      = BleHandler(self.settings, hciIndex)
        
    def shutDown(self):
        self.ble.shutDown()
    
    def setSettings(self, adminKey, memberKey, guestKey, referenceId="PythonLib", encryptionEnabled=True):
        self.settings.loadKeys(encryptionEnabled, adminKey, memberKey, guestKey, referenceId)
        
        
    def loadSettingsFromFile(self, path):
        fileReader = JsonFileStore(path)
        data = fileReader.getData()
        
        if "admin" not in data:
            raise BluenetBleException(BluenetError.ADMIN_KEY_REQURED)
        if "member" not in data:
            raise BluenetBleException(BluenetError.MEMBER_KEY_REQUIRED)
        if "guest" not in data:
            raise BluenetBleException(BluenetError.GUEST_KEY_REQURED)
        
        self.setSettings(data["admin"], data["member"], data["guest"])
        

    def connect(self, address):
        self.ble.connect(address)
        if self.settings.encryptionEnabled:
            try:
                self.control.getAndSetSessionNone()
            except BluenetBleException as err:
                # the only relevant error here is this one. If it is any other, the Crownstone is in the wrong mode
                if err.type is BleError.COULD_NOT_VALIDATE_SESSION_NONCE:
                    raise err

    def setupCrownstone(self, address, crownstoneId, meshAccessAddress, ibeaconUUID, ibeaconMajor, ibeaconMinor):
        self.connect(address)
        self.setup.setup(crownstoneId, meshAccessAddress, ibeaconUUID, ibeaconMajor, ibeaconMinor)
        self.disconnect()
        
    
    def disconnect(self):
        self.ble.disconnect()
    
    def startScanning(self, scanDuration=3):
        self.ble.startScanning(scanDuration)

    def stopScanning(self):
        self.ble.stopScanning()

    def getCrownstonesByScanning(self, scanDuration=3):
        gatherer = Gatherer()
    
        subscriptionIdValidated = BluenetEventBus.subscribe(Topics.advertisement,             lambda advertisementData: gatherer.handleAdvertisement(advertisementData, True)  )
        subscriptionIdAll       = BluenetEventBus.subscribe(SystemBleTopics.rawAdvertisement, lambda advertisementData: gatherer.handleAdvertisement(advertisementData, False) )
    
        self.ble.startScanning(scanDuration=scanDuration)
    
        BluenetEventBus.unsubscribe(subscriptionIdValidated)
        BluenetEventBus.unsubscribe(subscriptionIdAll)
        
        return gatherer.getCollection()
        
    
    def getNearestCrownstone(self, rssiAtLeast=-100, scanDuration=3, returnFirstAcceptable=False, addressesToExclude=[]):
        return self._getNearest(False, rssiAtLeast, scanDuration, returnFirstAcceptable, False, addressesToExclude)
    
    
    def getNearestValidatedCrownstone(self, rssiAtLeast=-100, scanDuration=3, returnFirstAcceptable=False, addressesToExclude=[]):
        return self._getNearest(False, rssiAtLeast, scanDuration, returnFirstAcceptable, True, addressesToExclude)
    
    
    def getNearestSetupCrownstone(self, rssiAtLeast=-100, scanDuration=3, returnFirstAcceptable=False, addressesToExclude=[]):
        return self._getNearest(True, rssiAtLeast, scanDuration, returnFirstAcceptable, True, addressesToExclude)
    

    def _getNearest(self, setup, rssiAtLeast, scanDuration, returnFirstAcceptable, validated, addressesToExclude):
        addressesToExcludeSet = set()
        for data in addressesToExclude:
            if isinstance(data, dict):
                if "address" in data:
                    addressesToExcludeSet.add(data["address"].lower())
                else:
                    raise BluenetException(BluenetError.INVALID_ADDRESS, "Addresses to Exclude is either an array of addresses (like 'f7:19:a4:ef:ea:f6') or an array of dicts with the field 'address'")
            else:
                addressesToExcludeSet.add(data.lower())
        
        selector = NearestSelector(setup, rssiAtLeast, returnFirstAcceptable, addressesToExcludeSet)
    
        topic = Topics.advertisement
        if not validated:
            topic = SystemBleTopics.rawAdvertisement
    
        subscriptionId = BluenetEventBus.subscribe(topic, selector.handleAdvertisement)
        
        self.ble.startScanning(scanDuration=scanDuration)
    
        BluenetEventBus.unsubscribe(subscriptionId)
        
        return selector.getNearest()