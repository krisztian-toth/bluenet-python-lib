from enum import Enum


class SystemBleTopics(Enum):
    rawAdvertisement = "rawAdvertisement"  # used to propagate verified state messages through the system
