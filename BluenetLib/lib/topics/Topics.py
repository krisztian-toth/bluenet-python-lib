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
    newCrownstoneFound = "newCrownstoneFound"  # data is single value: id: int
    powerUsageUpdate = "powerUsageReal"  # data is dictionary: { id: int, powerUsage  : number }
    switchStateUpdate = "switchState"  # data is dictionary: { id: int, switchState : number }

    advertisement = "advertisement" # data is dictionary {
                                    #   name: string
                                    #   rssi: int
                                    #   address: string   # mac address
                                    #   serviceUUID: string
                                    #   serviceData: {
                                    #     opCode:                       int
                                    #     dataType:                     int
                                    #     stateOfExternalCrownstone:    int    # adv contains state of external crownstone
                                    #     hasError:                     bool   # this crownstone has an error
                                    #     setupMode:                    bool   # is in setup mode
                                    #     id:                           int    # crownstone id (0-255)
                                    #     switchState:                  int
                                    #     flagsBitmak:                  int
                                    #     temperature:                  int    # chip temp
                                    #     powerFactor:                  int    # factor between real and appearent
                                    #     powerUsageReal:               int    # usage in watts (W)
                                    #     powerUsageApparent:           int    # usage in VA
                                    #     accumulatedEnergy:            int
                                    #     timestamp:                    int    # time on Crownstone seconds since epoch with locale correction
                                    #     dimmingAvailable:             bool   # dimming is available for use (it is not in the first 60 seconds after boot)
                                    #     dimmingAllowed:               bool   # this Crownstone can dim
                                    #     switchLocked:                 bool   # this Crownstone is switch-locked
                                    #     errorMode:                    bool   # advertisement type errorMode : the errors JSON is valid. This alternates with normal advertisements
                                    #     errors: {
                                    #         overCurrent:              bool
                                    #         overCurrentDimmer:        bool
                                    #         temperatureChip:          bool
                                    #         temperatureDimmer:        bool
                                    #         dimmerOnFailure:          bool
                                    #         dimmerOffFailure:         bool
                                    #         bitMask:                  int
                                    #     }
                                    #     uniqueElement:                int    # something that identifies this advertisement uniquely. Can be used to skip duplicate payloads
                                    #     timeIsSet:                    bool   # this crownstone knows what time it is
                                    # }

    personEnteredLocation = "personEnteredLocation" # data is dictionary: {"locationId": str, "name": str, "person": {"id": str, "email": str, "name": str}}
    personLeftLocation = "personLeftLocation" # data is dictionary: {"locationId": str, "name": str, "person": {"id": str, "email": str, "name": str}}
    uartMessage = "uartMessage" # data is dictionary: {"string": str, "data": [uint8, uint8, ...] }

