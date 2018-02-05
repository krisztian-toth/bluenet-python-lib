from lib.util.Conversion import Conversion

class PowerCalculationPacket:
	amountOfSamples = 9
	sampleSize = 4
	packetSize = amountOfSamples * sampleSize

	currentRmsMA               = 0
	currentRmsMedianMA         = 0
	filteredCurrentRmsMA       = 0
	filteredCurrentRmsMedianMA = 0
	avgZeroVoltage             = 0
	avgZeroCurrent             = 0
	powerMilliWattApparent     = 0
	powerMilliWattReal 	       = 0
	avgPowerMilliWattReal      = 0

	def __init__(self, payload):
		if len(payload) < self.packetSize:
			print("ERROR: INVALID PAYLOAD LENGTH", len(payload), payload)
			return

		i = 0
		self.currentRmsMA 				= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.currentRmsMedianMA 		= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.filteredCurrentRmsMA 		= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.filteredCurrentRmsMedianMA = Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.avgZeroVoltage 			= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.avgZeroCurrent 			= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.powerMilliWattApparent 	= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.powerMilliWattReal 		= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])
		i += self.sampleSize

		self.avgPowerMilliWattReal 		= Conversion.uint8_array_to_int32(payload[i:i+self.sampleSize])

	def getDict(self):
		dict = {}

		dict["crownstoneId"] = 0  # TODO: get the Crownstone ID here.
		dict["currentRmsMA"] = self.currentRmsMA
		dict["currentRmsMedianMA"] = self.currentRmsMedianMA
		dict["filteredCurrentRmsMA"] = self.filteredCurrentRmsMA
		dict["filteredCurrentRmsMedianMA"] = self.filteredCurrentRmsMedianMA
		dict["avgZeroVoltage"] = self.avgZeroVoltage
		dict["avgZeroCurrent"] = self.avgZeroCurrent
		dict["powerMilliWattApparent"] = self.powerMilliWattApparent
		dict["powerMilliWattReal"] = self.powerMilliWattReal
		dict["avgPowerMilliWattReal"] = self.avgPowerMilliWattReal

		return dict