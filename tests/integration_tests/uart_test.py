import signal
from random import randint

# lets start all modules one by one.
from lib.core.uart.UartBridge import UartBridge

from BluenetLib.lib.util import Conversion
from BluenetLib.lib.util import SystemTopics, eventBus
from BluenetLib.lib.util import UartUtil


class UartTest:
	runTest = True

	def __init__(self):
		uartListener = UartBridge()
		# start listener for SIGINT kill command
		signal.signal(signal.SIGINT, self.stopAll)

		# start processes
		uartListener.start()


	# make sure everything is killed and cleaned up on abort.
	def stopAll(self, signal, frame):
		eventBus.emit(SystemTopics.cleanUp)
		self.runTest = False
		exit(0)



	def genMsg(self):
		# Random payload
		payloadLen = randint(0, 122)
		payload=[]
		for i in range(0, payloadLen):
			payload.append(randint(0, 255))
		opCode = randint(0, 2**16-1)

		# Control packet
		opCode = 0
		ctrlPayload = []

		# Keepalive
		ctrlType = 6
		ctrlPayload.append(1)
		ctrlPayload.append(100)
		ctrlPayload.extend(Conversion.uint16_to_uint8_array(2**16-1))

		payload = [ctrlType, 0]
		payload.extend(Conversion.uint16_to_uint8_array(len(ctrlPayload)))
		payload.extend(ctrlPayload)

		msg = []
		msg.extend(Conversion.uint16_to_uint8_array(opCode))
		msg.extend(Conversion.uint16_to_uint8_array(len(payload)))
		msg.extend(payload)
		crc = UartUtil.crc16_ccitt(msg, len(msg))
		msg.extend(Conversion.uint16_to_uint8_array(crc))
		escapedMsg = UartUtil.uartEscape(msg)

		# Insert start char
		arr8 = []
		if randint(0,3):
			arr8.append(UartUtil.UART_START_CHAR)

		arr8.extend(escapedMsg)
		byteArray = bytes(arr8)
		print("payload size=", len(payload))
		print("crc=", crc)
		print("arr8=")
		hexString = Conversion.uint8_array_to_hex_string(arr8)
		hexString = ' '.join(hexString[i:i+2] for i in range(0, len(hexString), 2))
		print(hexString)
		return byteArray

	def run(self):
		while self.runTest:
			inputStr = input("input plz")
			byteArray = self.genMsg()
			eventBus.emit(SystemTopics.uartWriteData, byteArray)