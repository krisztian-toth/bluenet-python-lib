# Bluenet BLE

### This only works on linux due to the usage of BlueZ.


Since the Crownstone communicates through BLE, we can use BLE to tell it to do things!

This library works with Python 3.5 and higher. It does not work with Python 3.4...

# Requirements

We need libbluetooth-dev for developing with BLE.

```
sudo apt-get install libbluetooth-dev libglib2.0-dev
```

# Installing Bluenet BLE

You can use the setupBLE.py to install Bluenet + BluenetBLE. If you are on other platforms than Linux, you can use setup.py to install just Bluenet.

```
sudo python3 setupBLE.py install
```


# Documentation

To use Bluenet BLE, you first import it from Bluenetlib.

```python
from BluenetLib.BLE import BluenetBle
```

BluenetBle is composed of a number of top level methods and modules for specific commands. We will first describe these top level methods.

##### `shutDown()`
> Shut down the BLE module. This is should be done on closing your script

##### `setSettings(adminKey: string, memberKey: string, guestKey: string, referenceId="PythonLib", encryptionEnabled=True)`
> The Crownstone uses encryption by default. There are 3 keys used. You can find more information on that in the [protocol](https://github.com/crownstone/bluenet/blob/master/docs/PROTOCOL.md).
These keys are 16 characters long like "adminKeyForCrown" or 32 characters as a hex string like "9332b7abf19b86ff48156d88c687def6". The referenceId is optional. If you know what you're doing, you can disable the encryption but it should never be required.


##### `loadSettingsFromFile(path: string)`
> As an alternative to using setSettings, you can load it from a json file. The path is relative to the script being executed. An example of this json file is:
>```
>{
>  "admin":  "adminKeyForCrown",
>  "member": "memberKeyForHome",
>  "guest":  "guestKeyForOther"
>}
>```

##### `connect(address: string)`
> This will connect to the Crownstone with the provided MAC address. You get get this address by scanning or getting the nearest Crownstone. More on this below.

##### `setupCrownstone(address: string, crownstoneId: int, meshAccessAddress: string, ibeaconUUID: string, ibeaconMajor: uint16, ibeaconMinor: uint16)`
> New Crownstones are in setup mode. In this mode they are open to receiving encryption keys. This method facilitates this process. No manual connection is required.
> - address is the MAC address.
> - crownstoneId is a uint8 id for this Crownstone
> - meshAccessAddress is a uint32 with a number of requirements. All Crownstones with a shared meshAccessAddress can receive each others messages. Keep in mind that they need a shared keyset to understand the messages. To facilitate the creation of an access address, there is a util function available. More on this at the Util section.
> - ibeaconUUID is a string like "d8b094e7-569c-4bc6-8637-e11ce4221c18"
> - ibeaconMajor is a number between 0 and 65535
> - ibeaconMinor is a number between 0 and 65535

##### `disconnect()`
> This will disconnect from the connected Crownstone.

##### `startScanning(timeout=3)`
> This will start scanning for Crownstones in a background thread. The timeout denotes how long we will scan for. Once scanning is active, Topic.advertisement events will be triggered with the advertisements of the Crownstones that share our encryption keys or are in setup mode.

##### `stopScanning()`
> This will stop an active scan.

##### `getNearestCrownstone(rssiAtLeast=-100, timeout=3, returnFirstAcceptable=False)`
> This will search for the nearest Crownstone. It will return ANY Crownstone, not just the ones sharing our encryption keys.
> - rssiAtLeast, you can use this to indicate a maximum distance
> - timeout, the amount of time we scan
> - returnFirstAcceptable, if this is True, we return on the first Crownstone in the rssiAtLeast range. If it is False, we will scan for the timeout duration and return the closest one.

##### `getNearestValidatedCrownstone(rssiAtLeast=-100, timeout=3, returnFirstAcceptable=False)`
> Same as getNearestCrownstone but will only search for Crownstones with the same encryption keys.

##### `getNearestSetupCrownstone(rssiAtLeast=-100, timeout=3, returnFirstAcceptable=False)`
> Same as getNearestCrownstone but will only search for Crownstones in setup mode.


## Control Module

The modules contain groups of methods. You can access them like this:
```python
from BluenetLib.BLE import BluenetBle

# initialize the Bluetooth Core
bluenetBle = BluenetBle()

# set the switch stat eusing the control module
bluenetBle.connect(address)
bluenetBle.control.setSwitchState(0)
bluenetBle.disconnect()
```


Methods:

##### `setSwitchState(switchState: float)`
> You can switch the Crownstone. 0 for off, 1 for on, between 0 and 1 to dim. If you want to dim, make sure dimming is enabled. You can enable this using the allowDimming method.
##### `switchRelay(switchState)`
> DEVELOPMENT ONLY: you can switch the relay. 0 for off, 1 for on. Use the setSwitchState instead.
##### `switchPWM(switchState)`
> DEVELOPMENT ONLY: you can switch the IGBTs. 0 for off, 1 for on, in between for dimming. Use the setSwitchState instead.
##### `commandFactoryReset()`
> Assuming you have the encryption keys, you can use this method to put the Crownstone back into setup mode.
##### `allowDimming(allow: bool)`
> Enable or disable dimming on this Crownstone. Required if you want to dim with setSwitchState.
##### `disconnect()`
> Tell the Crownstone to disconnect from you. This can help if your Bluetooth stack does not reliably disconnect.
##### `lockSwitch(lock: bool)`
> Lock the switch. If locked, it's switchState cannot be changed.
##### `reset()`
> Restart the Crownstone.


## State Module

This is used to get state variables from the Crownstone. [https://github.com/crownstone/bluenet/blob/master/docs/PROTOCOL.md#state-packet-1]

The modules contain groups of methods. You can access them like this:
```python
from BluenetLib.BLE import BluenetBle

# initialize the Bluetooth Core
bluenetBle = BluenetBle()

# set the switch stat eusing the control module
bluenetBle.connect(address)
switchstate = bluenetBle.state.getSwitchState()
bluenetBle.disconnect()
```


##### `getSwitchState()`
> Get the switch state in the raw form [https://github.com/crownstone/bluenet/blob/master/docs/PROTOCOL.md#switch_state_packet]
##### `getSwitchStateFloat()`
> Get the switchState in the range [0 .. 1]
##### `getTime()`
> Get the time on the Crownstone as a timestamp since epoch in seconds. This has been corrected for location.

## Util

Util contains a number (one right now) methods that will help you use the lib.

##### generateMeshAccessAddress()
> Generate the mesh access address used in the setup. It adheres to the requirements as per the Bluetooth spec:
> BLE specification's rules are defined in Core spec 4.2 Vol. 6 Part B Chapter 2.1.2 and are as follows:
> The initiator shall ensure that the Access Address meets the following requirements:
> - It shall not be the advertising channel packets’ Access Address.
> - It shall not have all four octets equal.
> - It shall not be a sequence that differs from the advertising channel packets’ Access Address by only one bit.
> - It shall have no more than six consecutive zeros or ones.
> - It shall have no more than 24 transitions.
> - It shall have a minimum of two transitions in the most significant six bits.

```python
from BluenetLib import Util

accessAddress = Util.generateMeshAccessAddress()
```

## EventBus

You can obtain the eventbus directly from the lib:

```
from BluenetLib import BluenetEventBus, Topics
```

##### `subscribe(TopicName: enum, functionPointer)`
> Returns a subscription ID that can be used to unsubscribe again with the unsubscribe method

##### `unsubscribe(subscriptionId: number)`
> This will stop the invocation of the function you provided in the subscribe method, unsubscribing you from the event.

These can be used like this:

```python

# simple example function to print the data you receive
def advertisementPrinter(data):
    print(data)

# subscribe to the powerUsageUpdate event
subscriptionId = BluenetEventBus.subscribe(Topics.advertisement, advertisementPrinter)

# unsubscribe again
BluenetEventBus.unsubscribe(subscriptionId)
```

## Events

These events are available for the BLE part of this lib:

##### `Topics.advertisement`
> Data format is:
>```python
> data is dictionary {
>   name: string
>   rssi: int
>   address: string   # mac address
>   serviceUUID: string
>   serviceData: {
>     opCode:                       int
>     dataType:                     int
>     stateOfExternalCrownstone:    int    # adv contains state of external crownstone
>     hasError:                     bool   # this crownstone has an error
>     setupMode:                    bool   # is in setup mode
>     id:                           int    # crownstone id (0-255)
>     switchState:                  int
>     flagsBitmak:                  int
>     temperature:                  int    # chip temp
>     powerFactor:                  int    # factor between real and appearent
>     powerUsageReal:               int    # usage in watts (W)
>     powerUsageApparent:           int    # usage in VA
>     accumulatedEnergy:            int
>     timestamp:                    int    # time on Crownstone seconds since epoch with locale correction
>     dimmingAvailable:             bool   # dimming is available for use (it is not in the first 60 seconds after boot)
>     dimmingAllowed:               bool   # this Crownstone can dim
>     switchLocked:                 bool   # this Crownstone is switch-locked
>     errorMode:                    bool   # advertisement type errorMode : the errors JSON is valid. This alternates with normal advertisements
>     errors: {
>         overCurrent:              bool
>         overCurrentDimmer:        bool
>         temperatureChip:          bool
>         temperatureDimmer:        bool
>         dimmerOnFailure:          bool
>         dimmerOffFailure:         bool
>         bitMask:                  int
>     }
>     uniqueElement:                int    # something that identifies this advertisement uniquely. Can be used to skip duplicate payloads
>     timeIsSet:                    bool   # this crownstone knows what time it is
> }
>```



# Troubleshooting

### installation
old request module (ImportError: cannot import name 'DependencyWarning') --> check [https://github.com/nickoala/telepot/issues/80]

cant find bluetooth.h --> install libbluetooth-dev

cant find bswap_128 --> happens on raspberry pi 3, check [https://github.com/labapart/gattlib/issues/6]

ZipImportError: bad local file header --> update python-setuptools

### running
Something about threading when setup is complete --> you don't have Python 3.5

