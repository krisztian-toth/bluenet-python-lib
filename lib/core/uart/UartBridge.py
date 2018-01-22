import json
import threading

import serial

from lib.core.uart.UartReader import UartReader
from lib.core.uart.UartWriter import UartWriter

class UartBridge (threading.Thread):
	baudrate = 38400
	port = 'COM1'
	serialController = None

	reader = None
	writer = None

	def __init__(self):
		threading.Thread.__init__(self)
		self.readConfig()
		self.startSerial()

	def run(self):
		print("RUNNING UartBridge THREAD")
		self.reader = UartReader(self.serialController)
		self.writer = UartWriter(self.serialController)

		self.reader.start()
		self.writer.start()




	def readConfig(self):
		with open('uart_config.json', 'r') as f:
			config = json.load(f)

		self.baudrate = config['serial']['baudrate']
		self.port = config['serial']['port']


	def startSerial(self):
		print("initializing serial with ", self.port, ' and ', self.baudrate)
		self.serialController = serial.Serial()
		self.serialController.port = self.port
		self.serialController.baudrate = int(self.baudrate)
		self.serialController.timeout = 0
		self.serialController.open()


