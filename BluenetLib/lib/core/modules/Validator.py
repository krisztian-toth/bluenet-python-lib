
from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.core.modules.StoneTracker import StoneTracker
from BluenetLib.lib.topics.SystemBleTopics import SystemBleTopics
from BluenetLib.lib.topics.Topics import Topics


class Validator:
    trackedCrownstones = {}
    
    def __init__(self):
        BluenetEventBus.subscribe(SystemBleTopics.rawAdvertisement, self.checkAdvertisement)
    
    def removeStone(self, address):
        del self.trackedCrownstones[address]
    
    def checkAdvertisement(self, advertisement):
        if advertisement.address not in self.trackedCrownstones:
            self.trackedCrownstones[advertisement.address] = StoneTracker(lambda: self.removeStone(advertisement.address))
            
        self.trackedCrownstones[advertisement.address].update(advertisement)
        
        if self.trackedCrownstones[advertisement.address].verified:
            BluenetEventBus.emit(Topics.advertisement, advertisement.getDictionary())
            
        