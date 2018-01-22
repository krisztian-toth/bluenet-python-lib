import threading

from lib.core.uart.UartReadBuffer import UartReadBuffer
from lib.util.EventBus import eventBus, Topics


class UartReader (threading.Thread):
	serialController = None
	running = True

	def __init__(self, serialController):
		threading.Thread.__init__(self)
		self.serialController = serialController


	def run(self):
		print("RUNNING UartReader THREAD")
		eventBus.on(Topics.cleanUp, self.stop)

		self.startReading()

	def stop(self, source):
		print("Killing uart listener")
		self.running = False


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
