

class ControlHandler:

	def __init__(self):
		pass

	def allowDimming(self):
		pass


# Bluenet.setSwitch(cid1, 1)
# Bluenet.setSwitch(cid2, 1)
# Bluenet.setSwitch(cid3, 1)
#
# Bluenet.getLoop()
# canDim = await Bluenet.canItDim(cid1)
# if canDim:
# 	await Bluenet.dim(cid1,0.65)
# else:
# 	await Bluenet.allowDimming(cid1, 1, verify=True, timeout= 10)
# 	await Bluenet.dim(cid1,0.65)
# Bluenet.runLoop()
#
#
# Bluenet.updateSettings({"dimmableCrownstones": [1,2,3,4], "lockedCrownstones": [5,6]})
# Bluenet.updateSettings({"lockedCrownstones": [5]})