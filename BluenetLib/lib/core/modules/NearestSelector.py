from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.topics.SystemBleTopics import SystemBleTopics


class NearestSelector:
    setupModeOnly = False
    rssiAtLeast = -100
    returnFirstAcceptable = False
    
    deviceList = []
    
    nearest = None
    
    def __init__(self, setupModeOnly=False, rssiAtLeast=-100, returnFirstAcceptable=False):
        self.setupModeOnly = setupModeOnly
        self.rssiAtLeast = rssiAtLeast
        self.returnFirstAcceptable = returnFirstAcceptable
        
    def handleAdvertisement(self, advertisement):
        if "serviceData" not in advertisement:
            return
        
        if self.setupModeOnly and not advertisement["serviceData"]["setupMode"]:
            return
        
        
        if not self.setupModeOnly and advertisement["serviceData"]["setupMode"]:
            return
            
            
        if advertisement["rssi"] < self.rssiAtLeast:
            return
        
        self.deviceList.append(advertisement)
        
        if self.returnFirstAcceptable:
            BluenetEventBus.emit(SystemBleTopics.abortScanning, True)
            
        
        
        
            
    def getNearest(self):
        
        if len(self.deviceList) == 0:
            return None
        
        nearest = self.deviceList[0]
        
        for adv in self.deviceList:
            if nearest["rssi"] < adv["rssi"] < 0:
                nearest = adv
            
        return {
            "name": nearest["name"],
            "address": nearest["address"],
            "rssi" : nearest["rssi"],
            "setupMode": nearest["serviceData"]["setupMode"],
            "id" : nearest["serviceData"]["id"]
        }
        
        
        
        