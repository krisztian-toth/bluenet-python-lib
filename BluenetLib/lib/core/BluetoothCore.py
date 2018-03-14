from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.core.bluenet_modules.BleHandler import BleHandler
from BluenetLib.lib.core.bluenet_modules.ControlHandler import ControlHandler
from BluenetLib.lib.core.bluenet_modules.SetupHandler import SetupHandler


class BluetoothCore:
    control = None
    setup   = None
    config  = None
    state   = None
    mesh    = None
    
    _ble    = None
    
    def __init__(self):
        self.control = ControlHandler()
        self.setup   = SetupHandler()
        self._ble    = BleHandler()
        
    
    def connect(self, address):
        pass
    
    def startScanning(self):
        self._ble.startScanning()

    def startScanningForCrownstones(self):
        self._ble.startScanning()
    
    def stopScanning(self):
        self._ble.stopScanning()
    
    