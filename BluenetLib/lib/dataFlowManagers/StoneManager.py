from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.dataFlowManagers.StoneStateManager import StoneStateManager
from BluenetLib.lib.topics.SystemCloudTopics import SystemCloudTopics
from BluenetLib.lib.topics.Topics import Topics


class StoneManager:
    stones = {}
    stateManager = None
    
    def __init__(self):
        self.stateManager = StoneStateManager()
        BluenetEventBus.subscribe(Topics.newCrownstoneFound, self.handleNewStoneFromScan)
        BluenetEventBus.subscribe(SystemCloudTopics.stoneDownloadedFromCloud, self.handleStoneFromCloud)
        
        
    def getIds(self):
        ids = []
        
        for stoneId, data in enumerate(self.stones):
            ids.append(stoneId)
        
        return ids
    
    
    def getStones(self):
        return self.stones
    
    
    def handleNewStoneFromScan(self, stoneId):
        if stoneId in self.stones:
            self.stones[stoneId]["available"] = True
        else:
            self.stones[stoneId] = {"available": True}
            
        BluenetEventBus.subscribe(Topics.crownstoneAvailable, self.stones[stoneId])
        
            
    def handleStoneFromCloud(self, stoneData):
        stoneId = stoneData["id"]
        
        available = False
        if stoneId in self.stones:
            available = self.stones[stoneId]["available"]
        
        self.stones[stoneId] = stoneData
        self.stones[stoneId]["available"] = available
        
        
    
    
    