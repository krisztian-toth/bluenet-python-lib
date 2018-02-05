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
		dict = {}

		dict["crownstoneId"] = 0 # TODO: get the Crownstone ID here.
		dict["type"] = self.typeDescription
		dict["data"] = self.samples

		return dict