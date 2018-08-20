from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.topics.SystemTopics import SystemTopics
from BluenetLib.lib.topics.Topics import Topics


class StoneStateManager:
    def __init__(self):
        self.stones = {}
        BluenetEventBus.subscribe(SystemTopics.stateUpdate, self.handleStateUpdate)

    def handleStateUpdate(self,data):
        stoneId = data[0]
        state = data[1]

        if stoneId in self.stones:
            if self.stones[stoneId]["timestampLastSeen"] < state.timestamp:
                self.stones[stoneId]["timestampLastSeen"] = state.timestamp
                self.stones[stoneId]["data"] = data[1].getDict()
                self.emitNewData(data)
        else:
            BluenetEventBus.emit(Topics.newCrownstoneFound, data[0])
            self.stones[stoneId] = {"timestampLastSeen":state.timestamp, "data": data[1].getDict()}
            self.emitNewData(data)
    
    def emitNewData(self, data):
        BluenetEventBus.emit(Topics.powerUsageUpdate,  {"id": data[0], "powerUsage":  data[1].powerUsageReal})
        BluenetEventBus.emit(Topics.switchStateUpdate, {"id": data[0], "switchState": data[1].switchState})

    def getIds(self):
        ids = []
        for stoneId, stoneData in self.stones.items():
            ids.append(stoneId)

        return ids
