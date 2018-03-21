import time

from BluenetLib import CrownstoneCloud, Bluenet, BluenetEventBus, Topics

bluenet = Bluenet(catchSIGINT=True)
cloud = CrownstoneCloud()

cloud.loadConfigFromFile('user.json')

sphereHandler = cloud.getSphereHandler('58de6bda62a2241400f10c67')

def printEvent(topic, data):
    print("Got Event:", topic, data)

BluenetEventBus.subscribe(Topics.personEnteredLocation, lambda x: printEvent(Topics.personEnteredLocation, x))
BluenetEventBus.subscribe(Topics.personLeftLocation,    lambda x: printEvent(Topics.personLeftLocation, x))

print("Start Polling Presence")
sphereHandler.startPollingPresence()



