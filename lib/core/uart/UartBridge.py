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

	def __init__(self):
		threading.Thread.__init__(self)
		self.readConfig()
		self.startSerial()


	def run(self):
		print("RUNNING UartBridge THREAD")
		self.parser = UartParser()

		eventBus.on(SystemTopics.uartWriteData, self.writeToUart)

		self.startReading()

	def stop(self):
		self.running = False


	def readConfig(self):
		with open('uart_config.json', 'r') as f:
			config = json.load(f)

		self.baudrate = config['baudrate']
		self.port = config['port']


	def startSerial(self):
		print("initializing serial with ", self.port, ' and ', self.baudrate)
		self.serialController = serial.Serial()
		self.serialController.port = self.port
		self.serialController.baudrate = int(self.baudrate)
		self.serialController.timeout = 0
		self.serialController.open()


	def startReading(self):
		print("Starting reading the uart")
		readBuffer = UartReadBuffer()
		while self.running:
			byte  = self.serialController.read()
			if byte:
				readBuffer.add(byte)
			#print(byte)

		print("Cleaning up")
		self.serialController.close()

	def writeToUart(self, data):
		# print("Writing", data)
		self.serialController.write(data)
