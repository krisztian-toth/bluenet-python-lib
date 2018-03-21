from enum import Enum

class Topics(Enum):
    newCrownstoneFound = "newCrownstoneFound"  # data is single value: crownstoneId: int
    powerUsageUpdate = "powerUsageReal"  # data is dictionary: { crownstoneId: int, powerUsage  : number }
    switchStateUpdate = "switchState"  # data is dictionary: { crownstoneId: int, switchState : number }

    advertisement = "advertisement"

    personEnteredLocation = "personEnteredLocation" # data is dictionary: {"locationId": str, "name": str, "person": {"id": str, "email": str, "name": str}}
    personLeftLocation = "personLeftLocation" # data is dictionary: {"locationId": str, "name": str, "person": {"id": str, "email": str, "name": str}}

