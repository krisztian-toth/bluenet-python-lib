from lib.util.Conversion import Conversion

class CurrentSamplesPacket:

	NUM_SAMPLES = 100
	SAMPLES_SIZE = 2
	# PACKET_SIZE = NUM_SAMPLES * SAMPLES_SIZE
	PACKET_SIZE = 0

	samples = []

	def __init__(self, payload):
		self.PACKET_SIZE = self.NUM_SAMPLES * self.SAMPLES_SIZE
		if (len(payload) < self.PACKET_SIZE):
			print("ERROR: INVALID PAYLOAD LENGTH", len(payload), payload)
			return

		self.samples = []
		for i in range(0, self.PACKET_SIZE, 2):
			self.samples.append(Conversion.uint16_to_int16(Conversion.uint8_array_to_uint16(payload[i:i+2])))


class VoltageSamplesPacket:

	NUM_SAMPLES = 100
	SAMPLES_SIZE = 2
	# PACKET_SIZE = NUM_SAMPLES * SAMPLES_SIZE
	PACKET_SIZE = 0

	samples = []

	def __init__(self, payload):
		self.PACKET_SIZE = self.NUM_SAMPLES * self.SAMPLES_SIZE
		if (len(payload) < self.PACKET_SIZE):
			print("ERROR: INVALID PAYLOAD LENGTH", len(payload), payload)
			return

		self.samples = []
		for i in range(0, self.PACKET_SIZE, 2):
			self.samples.append(Conversion.uint16_to_int16(Conversion.uint8_array_to_uint16(payload[i:i+2])))

class PowerCalculationsPacket:
	PACKET_SIZE = 9*4

	currentRmsMA = 0
	currentRmsMedianMA = 0
	filteredCurrentRmsMA = 0
	filteredCurrentRmsMedianMA = 0
	avgZeroVoltage = 0
	avgZeroCurrent = 0
	powerMilliWattApparent = 0
	powerMilliWattReal = 0
	avgPowerMilliWattReal = 0

	def __init__(self, payload):
		if (len(payload) < self.PACKET_SIZE):
			print("ERROR: INVALID PAYLOAD LENGTH", len(payload), payload)
			return

		i=0
		self.currentRmsMA = Conversion.uint8_array_to_int32(payload[i:i+4])
		i+=4
		self.currentRmsMedianMA = Conversion.uint8_array_to_int32(payload[i:i+4])
		i+=4
		self.filteredCurrentRmsMA = Conversion.uint8_array_to_int32(payload[i:i+4])
		i+=4
		self.filteredCurrentRmsMedianMA = Conversion.uint8_array_to_int32(payload[i:i+4])
		i+=4
		self.avgZeroVoltage = Conversion.uint8_array_to_int32(payload[i:i+4])
		i+=4
		self.avgZeroCurrent = Conversion.uint8_array_to_int32(payload[i:i+4])
		i+=4
		self.powerMilliWattApparent = Conversion.uint8_array_to_int32(payload[i:i+4])
		i+=4
		self.powerMilliWattReal = Conversion.uint8_array_to_int32(payload[i:i+4])
		i+=4
		self.avgPowerMilliWattReal = Conversion.uint8_array_to_int32(payload[i:i+4])
		i+=4

