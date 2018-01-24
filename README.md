# bluenet-python-lib
Official Python lib for Crownstone. 

Currently this requires a "Crownstone Unified System Bridge", or **Crownstone USB**. 

The Bluetooth implementation will be added soon.


# Install guide

This module is written in Python 3 and needs Python 3.5 or higher. The reason for this is that most of the asynchronous processes use the embedded asyncio core library.

Pip is used for package management. You can install all dependencies by running:

```
pip install -r requirements.txt
```

Make sure pip here is for Python 3. If you're not sure, you can try running:

```
pip3 install -r requirements.txt
```

## Requirements for the Crownstone USB

### OS X
OS X requires installation of the SiliconLabs driver: [https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers)

### Ubuntu
In order to use serial without root access, you have to add yourself to the `dialout` group:
```
$ sudo adduser $USER dialout
```

### Raspbian
In order to use serial without root access, you have to add yourself to the `dialout` group:
```
$ sudo adduser $USER dialout
```



# Example

An example is provided in the root of this repository.

## Prerequisites

- First use the [phone app](https://crownstone.rocks/app) to setup your Crownstones and the Crownstone USB.
- Make sure you update the Crownstones' firmware to at least 2.0.0.
- Find out what port to use (e.g. `COM1`, `/dev/ttyUSB0`, or `/dev/tty.SLAB_USBtoUART`) and fill this in the example.py.
- Find out the ID of the Crownstone you want to switch: TODO


## Running

Run the example with python 3.

```
$ python example.py
```

Some systems may require calling python3 specifically:

```
$ python3 example.py
```

## The code

The example is shown below to get an idea of how everything works:

```python 
import time

from BluenetLib import Bluenet

def showPowerUsage(data):
	print("PowerUsage for CrownstoneId:", data["crownstoneId"], " is", data["powerUsage"], "W")

# create new instance of Bluenet
bluenet = Bluenet()

# start up the USB bridge
bluenet.initializeUsbBridge("/dev/tty.SLAB_USBtoUART")

#set up event listeners
eventBus = bluenet.getEventBus()
topics   = bluenet.getTopics()
eventBus.subscribe(topics.powerUsageUpdate, showPowerUsage)

# this is the id of the Crownstone we will be switching
targetCrownstoneId = 235

# switch this Crownstone 100 times on and off.
switchState = True
for i in range(0,100):
	if not bluenet.isRunning:
		break

	bluenet.switchCrownstone(targetCrownstoneId, on = switchState)
	if switchState:
		print("Switching Crownstone on  (iteration: ", i,")")
	else:
		print("Switching Crownstone off (iteration: ", i,")")

	switchState = not switchState
	time.sleep(2)
```



# Documentation

This lib is used to interpret the serial data from the Crownstone USB.

This library exposes the BluenetLib module. From this module you can use Bluenet.

```python

from BluenetLib import Bluenet
 
# this is what you will be working with:
myBluenetInstance = Bluenet()

```

## Switching Crownstones on, off and dimming

You can use your Bluenet instance to turn Crownstones on and off. This is done using the switchCrownstone function:

```python
# this Crownstone will be switched
targetCrownstoneId = 15
 
# turn on
myBluenetInstance.switchCrownstone(targetCrownstoneId, on = True)
 
# turn off
myBluenetInstance.switchCrownstone(targetCrownstoneId, on = False)
```

The Crownstone IDs range from 1 to 255. There is a limit of 255 Crownstones per Sphere. More on Spheres and Crownstone IDs can be found here: TODO.

To dim a Crownstone, you first need to tell it that is it allowed to dim. Currently this is done through the Crownstone app.
An API for this will be added shortly. When it is set to allow dimming, it can dim and switch up to 100 W devices.

You can dim your Crownstones with the dimCrownstone method:

```python

# any value between 0 and 1 can be used. 0 is off, 1 is on
myBluenetInstance.dimCrownstone(targetCrownstoneId, 0.5)

```

## Getting Data

The Bluenet python lib uses an event bus to deliver updates to you. You can request an instance of the event bus from Bluenet:

```python

# get an instance of the eventBus to subscribe to updates
myEventBus = myBluenetInstance.getEventBus()
 
# get an instance of the available Topics
theTopics = myBluenetInstance.getTopics()
```

You can use the event bus to subscribe to topics.
 
The following Topics are currently available:

| Event Enum Name | Description |
| :--------------- | :--------- |
| `newCrownstoneFound` | When the lib hears from a Crownstone that it has not heard from since the lib was started, this event is emitted. The data that is emitted is a single int which represents the Crownstone ID of the new Crownstone. |
| `powerUsageUpdate` | Every time a new data point is recorded, this event will notify the updated powerUsage value. The data that is emitted is a dictionary: `{ "crownstoneId": int, "powerUsage" :  float }`. |
| `switchStateUpdate` | Every time a new data point is recorded, this event will notify the updated powerUsage value. The data that is emitted is a dictionary: `{ "crownstoneId": int, "switchState" :  int [0 .. 128] }`. The switchState value is [explained here](https://github.com/crownstone/bluenet/blob/master/docs/PROTOCOL.md#switch_state_packet). |

## EventBus API

#### `subscribe(TopicName: enum, functionPointer)`
> Returns a subscription ID that can be used to unsubscribe again with the unsubscribe method

#### `unsubscribe(subscriptionId: number)`
> This will stop the invocation of the function you provided in the subscribe method, unsubscribing you from the event.

These can be used like this:

```python

# simple example function to print the data you receive
def dataPrinter(data):
    print(data)
    
# subscribe to the powerUsageUpdate event
subscriptionId = myEventBus.subscribe(myTopics.powerUsageUpdate, dataPrinter)
 
# unsubscribe again
myEventBus.unsubscribe(subscriptionId)


```

## Bluenet API

#### `initializeUsbBridge(port: string, catchSIGINT = True)`
> Sets up the communication with the Crownstone USB. 
> 
> The `port` is the port used by the serial communication. 
> For Windows devices this is commonly `COM1`, for Linux based system `/dev/ttyUSB0` and for OSX `/dev/tty.SLAB_USBtoUART`. Addresses and number can vary from system to system.
> The `catchSIGINT` argument (default: True) is used to ensure that (if True) the close command of a program (SIGINT), commonly triggered by Control+C, will cleanly close all UART connections before closing. If you want to do this manually, use the `stop` method.

#### `switchCrownstone(crownstoneId: int, on: Boolean)`
> Switch a Crownstone on and off

#### `dimCrownstone(crownstoneId: int, value: float [0 .. 1])`
> Dim the Crownstone. 0 is off, 1 is fully on. While dimming, the Crownstone is rated a maximum power usage of 100 W.

#### `getEventBus()`
> Get an instance of the EventBus used for data updates.

#### `getTopics()`
> Get an instance of the Topics : Enum available in the EventBus.

#### `getCrownstoneIds()`
> Get a list of the CrownstoneIDs (ints) that are known to the library.

#### `getLatestCrownstoneData(crownstoneId: int)`
> This will return a dictionary filled with all the information the library has on this Crownstone. This data will be extended in future versions. If the crownstoneId is unknown, ```None``` will be returned.
>
> Data Format:
> 
```
{
    "crownstoneId"       : int, ID of Crownstone. Range is [1 .. 255]
    "switchState"        : int, [explained here](https://github.com/crownstone/bluenet/blob/master/docs/PROTOCOL.md#switch_state_packet). Range is [0 .. 128]
    "flagBitMask"        : [explained here](https://github.com/crownstone/bluenet/blob/master/docs/PROTOCOL.md#flags_bitmask). Will be expanded upon in the future.
    "temperature"        : int, temperature of the chip of the Crownstone in Celsius
    "powerFactor"        : float, difference between real power usage (W) and apparent power usage (VA)
    "powerUsageReal"     : float, Real power usage in Watts (W)
    "powerUsageApparent" : float, Apparent power usage in VA
    "energyUsed"         : <unused> Will be functional in future versions of the firmware.
    "timestamp"          : float, seconds since Epoch with localization correction ( so if you are in GMT + 1, this will be 3600 higher than a normal UTC timestamp ). Time on Crownstone when this message was sent.
}
```

#### `stop()`
> Stop any running processes.

#### `isRunning()`
> Returns a Boolean indicating if the BluenetLib is running. This is relevant for the UART listener which communicates with the Crownstone USB.





# License

MIT


