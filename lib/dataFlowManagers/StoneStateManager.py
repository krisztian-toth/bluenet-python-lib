from lib.util.EventBus import eventBus, SystemTopics, Topics


class StoneStateManager:
	stones = {}

	def __init__(self):
		eventBus.subscribe(SystemTopics.stateUpdate, self.handleStateUpdate)

	def handleStateUpdate(self,data):
		stoneId = data[0]
		state = data[1]

		if stoneId in self.stones:
			if self.stones[stoneId]["timestampLastSeen"] < state.timestamp:
				self.stones[stoneId]["timestampLastSeen"] = state.timestamp
				self.stones[stoneId]["data"] = data[1].getDict()
				self.emitNewData(data)
		else:
			eventBus.emit(Topics.newCrownstoneFound, data[0])
			self.stones[stoneId] = {"timestampLastSeen":state.timestamp, "data": data[1].getDict()}
			self.emitNewData(data);

	def emitNewData(self, data):
		eventBus.emit(Topics.powerUsageUpdate,  {"crownstoneId": data[0], "powerUsage":  data[1].powerUsageReal})
		eventBus.emit(Topics.switchStateUpdate, {"crownstoneId": data[0], "switchState": data[1].switchState})

	def getIds(self):
		ids = []
		for stoneId, stoneData in self.stones.items():
			ids.append(stoneId)

		return ids

	def getLatestCrownstoneData(self, crownstoneId):
		if crownstoneId in self.stones:
			return self.stones[crownstoneId].data
		else:
			return None