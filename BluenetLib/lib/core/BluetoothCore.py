from BluenetLib.lib.util.JsonFileStore import JsonFileStore

from BluenetLib import BluenetBleException
from BluenetLib.Exceptions import BleError, BluenetError
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
    
    def __init__(self):
        self.settings = BluenetSettings()
        self.control  = ControlHandler(self)
        self.setup    = SetupHandler(self)
        self.state    = StateHandler(self)
        self.ble      = BleHandler(self.settings)
        
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
    
    def startScanning(self):
        self.ble.startScanning()

    def startScanningForCrownstones(self):
        self.ble.startScanning()
    
    def stopScanning(self):
        self.ble.stopScanning()

    
    def getNearestCrownstone(self, rssiAtLeast=-100, timeout=3, returnFirstAcceptable=False):
        return self._getNearest(False, rssiAtLeast, timeout, returnFirstAcceptable, False)
    
    
    def getNearestValidatedCrownstone(self, rssiAtLeast=-100, timeout=3, returnFirstAcceptable=False):
        return self._getNearest(False, rssiAtLeast, timeout, returnFirstAcceptable, True)
    
    
    def getNearestSetupCrownstone(self, rssiAtLeast=-100, timeout=3, returnFirstAcceptable=False):
        return self._getNearest(True, rssiAtLeast, timeout, returnFirstAcceptable, True)
    

    def _getNearest(self, setup, rssiAtLeast, timeout, returnFirstAcceptable, validated):
        selector = NearestSelector(setup, rssiAtLeast, returnFirstAcceptable)
    
        topic = Topics.advertisement
        if not validated:
            topic = SystemBleTopics.rawAdvertisement
    
        subscriptionId = BluenetEventBus.subscribe(topic, selector.handleAdvertisement)
        
        self.ble.startScanning(timeout=timeout)
    
        BluenetEventBus.unsubscribe(subscriptionId)
        
        return selector.getNearest()