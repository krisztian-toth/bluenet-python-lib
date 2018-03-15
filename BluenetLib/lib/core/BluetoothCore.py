from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.core.bluenet_modules.BleHandler import BleHandler
from BluenetLib.lib.core.bluenet_modules.ControlHandler import ControlHandler
from BluenetLib.lib.core.bluenet_modules.SetupHandler import SetupHandler
from BluenetLib.lib.core.bluenet_modules.StateHandler import StateHandler

from BluenetLib.lib.core.modules.BluenetSettings import BluenetSettings


class BluetoothCore:
    control = None
    setup   = None
    config  = None
    state   = None
    mesh    = None
    
    ble    = None
    
    
    
    def __init__(self):
        self.settings = BluenetSettings()
        self.control  = ControlHandler(self)
        self.setup    = SetupHandler(self)
        self.state    = StateHandler(self)
        self.ble      = BleHandler(self.settings)
        
    
    def setSettings(self, encryptionEnabled, adminKey, memberKey, guestKey, referenceId):
        self.settings.loadKeys(encryptionEnabled, adminKey, memberKey, guestKey, referenceId)
    
    def connect(self, address):
        self.ble.connect(address)
        if self.settings.encryptionEnabled:
            self.control.getAndSetSessionNone()

    
    def startScanning(self):
        self.ble.startScanning()

    def startScanningForCrownstones(self):
        self.ble.startScanning()
    
    def stopScanning(self):
        self.ble.stopScanning()
   