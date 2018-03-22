from enum import Enum

class Topics(Enum):
    crownstoneAvailable = "crownstoneAvailable"  # data is dictionary {
                                                 #     id: number
                                                 #     name: str
                                                 #     cloudId: str
                                                 #     address: str
                                                 #     type: str
                                                 #     dimmingEnabled: bool
                                                 #     major: number,
                                                 #     minor: number,
                                                 #     firmwareVersion: str
                                                 #  }
    newCrownstoneFound = "newCrownstoneFound"  # data is single value: crownstoneId: int
    powerUsageUpdate = "powerUsageReal"  # data is dictionary: { crownstoneId: int, powerUsage  : number }
    switchStateUpdate = "switchState"  # data is dictionary: { crownstoneId: int, switchState : number }

    advertisement = "advertisement"

    personEnteredLocation = "personEnteredLocation" # data is dictionary: {"locationId": str, "name": str, "person": {"id": str, "email": str, "name": str}}
    personLeftLocation = "personLeftLocation" # data is dictionary: {"locationId": str, "name": str, "person": {"id": str, "email": str, "name": str}}

