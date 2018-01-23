import json
import threading

import serial

from lib.core.uart.UartParser import UartParser
from lib.core.uart.UartReadBuffer import UartReadBuffer
from lib.util.EventBus import eventBus, SystemTopics


class UartBridge (threading.Thread):
	baudrate = 38400
	port = 'COM1'
	serialController = None
	parser = None

	running = True

	def __init__(self, port, baudrate):
		self.baudrate = baudrate
		self.port = port

		self.startSerial()
		threading.Thread.__init__(self)


	def run(self):
		eventBus.on(SystemTopics.uartWriteData, self.writeToUart)

		self.parser = UartParser()
		self.startReading()

	def stop(self):
		self.running = False


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
