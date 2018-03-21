import time

from BluenetLib import Cloud, Bluenet

bluenet = Bluenet(catchSIGINT=True)
cloud = Cloud()

cloud.loadConfigFromFile('user.json')

sphereHandler = cloud.getSphereHandler('58de6bda62a2241400f10c67')

def showEvent(topic, data):
    print("Topic", topic, data)

myEventBus = bluenet.getEventBus()
myTopics   = bluenet.getTopics()
myEventBus.subscribe(myTopics.personEnteredLocation, lambda x: showEvent(myTopics.personEnteredLocation, x))
myEventBus.subscribe(myTopics.personLeftLocation, lambda x: showEvent(myTopics.personLeftLocation, x))

print("Start Polling Presence")
sphereHandler.startPollingPresence(2)



