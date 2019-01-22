#!/usr/bin/env python3

"""An example that shows how to login to the cloud."""

from BluenetLib import CrownstoneCloud
from BluenetLib import BluenetEventBus, CloudTopics

cloud = CrownstoneCloud()

# Create a user.json with your login, see the readme.
cloud.loadUserConfigFromFile('user.json')

# Fill in the sphere id, see the readme.
sphereHandler = cloud.getSphereHandler('58de6bda62a2241400f10c67')

def printEvent(topic, data):
    print("Got Event:", topic, data)

BluenetEventBus.subscribe(CloudTopics.personEnteredLocation, lambda x: printEvent(CloudTopics.personEnteredLocation, x))
BluenetEventBus.subscribe(CloudTopics.personLeftLocation,    lambda x: printEvent(CloudTopics.personLeftLocation, x))

print("Start Polling Presence. Check if there are people present in this sphere using the consumer smart phone app. The enter end left events are thrown on changes.")
sphereHandler.startPollingPresence()



