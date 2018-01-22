import threading

import serial

from lib.util.EventBus import eventBus, Topics


class UartWriter (threading.Thread):
	serialController = None

	def __init__(self, serialController):
		threading.Thread.__init__(self)
		self.serialController = serialController

	def run(self):
		print("RUNNING UartWriter THREAD")
		eventBus.on(Topics.uartWriteData, self.writeToUart)

	def writeToUart(self, data):
		print("Writing", data)
		self.serialController.write(data)
