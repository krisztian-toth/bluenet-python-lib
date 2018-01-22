import uuid
from enum import Enum



class Topics(Enum):
    uartReadLine = 'uartReadLine'
    simulatedUartReadLine = 'simulatedUartReadLine'
    uartWriteCommand = 'uartWriteCommand'
    wsWriteMessage = 'wsWriteMessage'
    wsReceivedMessage = 'wsReceivedMessage'
    websocketConnectionInitialized = 'websocketConnectionInitialized'


class EventBus:
    topics = {}
    subscriberIds = {}

    def __init__(self):
        pass

    def on(self, topic, callback):
        print("subscribing", topic)
        if topic not in self.topics:
            self.topics[topic] = {}

        subscriptionId = str(uuid.uuid4())
        self.subscriberIds[subscriptionId] = topic
        self.topics[topic][subscriptionId] = callback

        return subscriptionId

    def emit(self, topic, data = True):
        if topic in self.topics:
            for subscriptionId in self.topics[topic]:
                self.topics[topic][subscriptionId](data)


    def off(self, subscriptionId):
        if subscriptionId in self.subscriberIds:
            topic = self.subscriberIds[subscriptionId]
            if topic in self.topics:
                self.topics[topic].pop(subscriptionId)

            self.subscriberIds.pop(subscriptionId)
        else:
            print("Subscription ID cannot be found.")


eventBus = EventBus()
