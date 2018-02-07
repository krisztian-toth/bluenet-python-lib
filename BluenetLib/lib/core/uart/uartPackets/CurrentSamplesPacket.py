from BluenetLib.lib.util.Conversion import Conversion

class CurrentSamplesPacket:

	amountOfSamples = 100
	sampleSize = 2
	packetSize = amountOfSamples * sampleSize

	typeDescription = 'current'

	samples = []

	def __init__(self, payload):
		if len(payload) < self.packetSize:
			print("ERROR: INVALID PAYLOAD LENGTH", len(payload), payload)
			return

		self.samples = []
		for i in range(0, self.packetSize, self.sampleSize):
			# we make this a list of tuples containing (time, data point)
			self.samples.append((0, Conversion.uint8_array_to_int16(payload[i:i+self.sampleSize])))

	def getDict(self):
		data = {}

		data["crownstoneId"] = 0 # TODO: get the Crownstone ID here.
		data["type"] = self.typeDescription
		data["data"] = self.samples

		return data