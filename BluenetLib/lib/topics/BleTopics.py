from enum import Enum

class BleTopics(Enum):
    advertisement         = "advertisement"         # data is single value: crownstoneId: int
    verifiedAdvertisement = "verifiedAdvertisement" # data is dictionary: { crownstoneId: int, powerUsage  : number }
    iBeaconAdvertisement  = "iBeaconAdvertisement"  # data is dictionary: { crownstoneId: int, switchState : number }

