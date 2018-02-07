import threading

import serial

from BluenetLib._EventBusInstance import BluenetEventBus
from BluenetLib.lib.core.uart.UartParser import UartParser
from BluenetLib.lib.core.uart.UartReadBuffer import UartReadBuffer
from BluenetLib.lib.topics.SystemTopics import SystemTopics


class UartBridge (threading.Thread):
	baudrate = 230400
	port = 'COM1'
	serialController = None
	parser = None
	eventId = 0

	running = True

	def __init__(self, port, baudrate):
		self.baudrate = baudrate
		self.port = port

		self.startSerial()
		threading.Thread.__init__(self)


	def run(self):
		self.eventId = BluenetEventBus.subscribe(SystemTopics.uartWriteData, self.writeToUart)
		self.parser = UartParser()
		self.startReading()

	def stop(self):
		self.running = False
		BluenetEventBus.unsubscribe(self.eventId)
	
	def startSerial(self):
		print("initializing serial on port ", self.port, ' with baudrate ', self.baudrate)
		self.serialController = serial.Serial()
		self.serialController.port = self.port
		self.serialController.baudrate = int(self.baudrate)
		self.serialController.timeout = 0
		self.serialController.open()


	def startReading(self):
		readBuffer = UartReadBuffer()
		while self.running:
			byte  = self.serialController.read()
			if byte:
				readBuffer.add(byte)
			#print(byte)

		print("Cleaning up")
		self.serialController.close()

	def writeToUart(self, data):
		self.serialController.write(data)
