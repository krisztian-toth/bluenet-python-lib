from bluepy.btle import Scanner

from BluenetLib.lib.core.bluetooth_delegates.ScanDelegate import ScanDelegate
from BluenetLib.lib.core.logic.Validator import Validator


class BleHandler:
    scanner = None
    
    def __init__(self):
        self.scanner = Scanner().withDelegate(ScanDelegate())
        self.validator = Validator()
    
    def connect(self):
        pass
    
    def startScanning(self):
        self.scanner.start()
        self.scanner.process(3)
        self.scanner.stop()

        
    
    def stopScanning(self):
        pass
    
    def readCharacteristic(self):
        pass
    
    def writeToCharacteristic(self):
        pass
    
    def enableNotifications(self):
        pass
    
    