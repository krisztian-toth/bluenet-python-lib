from lib.util.Conversion import Conversion

ESCAPE_TOKEN = 0x5c
BIT_FLIP_MASK = 0x40
START_TOKEN = 0x7e

class UartReadBuffer:

	buffer = []
	escapingNextToken = False
	active = False

	opCode = 0
	length = 0



	def __init__(self):
		pass

	def add(self, rawByte):
		print("working with", rawByte)

		byte = rawByte
		# first get the escaping out of the way to avoid any double checks later on
		if self.escapingNextToken:
			byte ^= BIT_FLIP_MASK
			print("ESCAPING BYTE")
			self.escapingNextToken = False

		# if we have a start token and we are not active
		if byte is START_TOKEN:
			if self.active:
				print("RESET: MULTIPLE START TOKENS")
				self.reset()
				return
			else:
				print("ACTIVATING")
				self.active = True
				return


		if not self.active:
			print("NOT ACTIVE")
			return

		if byte is ESCAPE_TOKEN:
			print("GOT ESCAPE TOKEN")
			self.escapingNextToken = True
			return



		self.buffer.append(byte)
		bufferSize = len(self.buffer)

		if bufferSize == 2:
			self.opCode = Conversion.uint8_array_to_uint16([self.buffer[0], self.buffer[1]])
			print("GOT OPCODE", self.opCode)
		elif bufferSize == 4:
			self.length = Conversion.uint8_array_to_uint16([self.buffer[2], self.buffer[3]])
			print("GOT length", self.length)
		elif bufferSize == (self.length + 2):
			self.process()
			return
		elif bufferSize > self.length + 2:
			print("OVERFLOW")
			self.reset()



	def process(self):
		# TODO: handle processed package
		print("GOT PAYLOAD", self.buffer)

		self.reset()


	def reset(self):
		self.buffer = []
		self.escapingNextToken = False
		self.active = False
		self.opCode = 0
		self.length = 0