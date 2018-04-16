from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.topics.SystemBleTopics import SystemBleTopics


class SetupChecker:
    address = None
    result = False
    
    def __init__(self, address):
        self.address = address
        
    def handleAdvertisement(self, advertisement):
        if "serviceData" not in advertisement:
            return
        
        if advertisement["address"] != self.address:
            return
        
        self.result = advertisement["serviceData"]["setupMode"]
    
    def getResult(self):
        return self.result