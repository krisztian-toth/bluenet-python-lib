from lib.util.EventBus import eventBus, SystemTopics, Topics


class StateUpdateManager:
	stones = {}

	def __init__(self):
		eventBus.on(SystemTopics.stateUpdate, self.handleStateUpdate)

	def handleStateUpdate(self,data):
		stoneId = data[0]
		state = data[1]

		if stoneId in self.stones:
			if self.stones[stoneId] < state.timestamp:
				self.stones[stoneId] = state.timestamp
				self.emitNewData(data)
		else:
			self.stones[stoneId] = state.timestamp
			self.emitNewData(data);

	def emitNewData(self, data):
		eventBus.emit(Topics.powerUsageUpdate, {"crownstoneId": data[0], "powerUsage": data[1].powerUsageReal})