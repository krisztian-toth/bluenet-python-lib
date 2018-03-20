import signal  # used to catch control C

from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.topics.Topics import Topics
from BluenetLib.lib.util.JsonFileStore import JsonFileStore

FILENAME = "BluenetDataStore.dat"

class StoreRecorder:
    store = None
    subscriptionId = None
    
    def __init__(self, filename=FILENAME):
        self.store = JsonFileStore(filename)
    
    def reset(self):
        self.store.clear()
        
    def subscribe(self):
        self.subscriptionId = BluenetEventBus.subscribe(Topics.newCrownstoneFound, self.handleNewCrownstone)
        
    def handleNewCrownstone(self, crownstoneId):
        self.store.addEntry(crownstoneId, True)