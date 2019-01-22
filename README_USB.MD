# Python Crownstone USB Library
Official Python lib for Crownstone: "Crownstone Unified System Bridge", or **Crownstone USB** implementation.

This works on all platforms and requires a **Crownstone USB** to work.

# Install guide

This module is written in Python 3 and needs Python 3.5 or higher. The reason for this is that most of the asynchronous processes use the embedded asyncio core library.

Pip is used for package management. You can install all dependencies by running:
```
python setup.py install

# or

python3 setup.py install
```

## Requirements for the Crownstone USB

### OS X
OS X requires installation of the SiliconLabs driver: [https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers)

### Ubuntu
In order to use serial without root access, you should be in the `dialout` group.

You can check if you're in the group:
```
$ groups
```

To add yourself:
```
$ sudo adduser $USER dialout
```

### Raspbian
Similar to Ubuntu.


# Example

An example is provided in the root of this repository.

## Prerequisites

- First use the [phone app](https://crownstone.rocks/app) to setup your Crownstones and the Crownstone USB.
- Make sure you update the Crownstones' firmware to at least 2.1.0.
- Find out what port to use (e.g. `COM1`, `/dev/ttyUSB0`, or `/dev/tty.SLAB_USBtoUART`) and fill this in at `discoveryExample.py` and `example.py` at the `initializeUSB` method.
- install the BluenetLib library using the setup.py:

```python
python3 setup.py install

# or:

python setup.py install
```

## Find the IDs of your Crownstones

Firstly run the example script that simply lists the IDs of the Crownstones. They are located in /examples/examplesUsb:
```
$ python3 discoveryExample.py
```

Some systems may require calling python3 specifically:
```
$ python3 discoveryExample.py
```

Once some IDs are printed, use one of them for the next example.


## Switch a Crownstone, and show power usage.

After filling in the port to use, and the Crownstone ID to switch, run the example with python 3:
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
#!/usr/bin/env python3

"""An example that switches a Crownstone, and prints the power usage of all Crownstones."""

import time, json
from BluenetLib import Bluenet, BluenetEventBus, UsbTopics

# Function that's called when the power usage is updated, a Crownstone is switched, or as an update every minute(ish).
def showNewData(data):
	print("New data received!")
	print(json.dumps(data, indent=2))
	print("-------------------")

# Create new instance of Bluenet
bluenet = Bluenet()

# Start up the USB bridge.
# Fill in the correct device, see the readme.
# For firmware versions below 2.1, add the parameter baudrate=38400
bluenet.initializeUSB("/dev/ttyUSB0")

# Set up event listeners
BluenetEventBus.subscribe(UsbTopics.newDataAvailable, showNewData)

# This is the id of the Crownstone we will be switching
targetCrownstoneId = 10

# Switch this Crownstone on and off.
switchState = True
for i in range(0,100):
	if not bluenet.running:
		break

	if switchState:
		print("Switching Crownstone on  (iteration: ", i,")")
	else:
		print("Switching Crownstone off (iteration: ", i,")")
	bluenet.switchCrownstone(targetCrownstoneId, on = switchState)

	switchState = not switchState
	time.sleep(2)


bluenet.stop()

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

## EventBus API

You can obtain the eventBus directly from the lib:

```
from BluenetLib import BluenetEventBus, UsbTopics
```

##### `subscribe(TopicName: enum, functionPointer)`
> Returns a subscription ID that can be used to unsubscribe again with the unsubscribe method

##### `unsubscribe(subscriptionId: number)`
> This will stop the invocation of the function you provided in the subscribe method, unsubscribing you from the event.

These can be used like this:

```python

# simple example function to print the data you receive
def showNewData(data):
	print("received new data: ", data)


# Set up event listeners
BluenetEventBus.subscribe(UsbTopics.newDataAvailable, showNewData) # keep in mind that this is using the UsbTopics, not the Topics

# unsubscribe again
BluenetEventBus.unsubscribe(subscriptionId)
```

## Events

These events are available for the USB part of the lib.

##### `UsbTopics.newDataAvailable`
> This is a topic with a summary of the data of a message received via the mesh. If you care about the power usage, you can get it from here. If the hasError: true, the accumulated energy is not filled, nor is the power factor and the powerUsageApparent.
> Data format is a dictionary with the fields shown below:
>```python
> {
>     id:                           int    # crownstone id (0-255)
>     setupMode:                    bool   # is in setup mode
>     switchState:                  int
>     temperature:                  int    # chip temp in Celcius
>     powerFactor:                  int    # factor between real and apparent
>     powerUsageReal:               int    # power usage in watts (W)
>     powerUsageApparent:           int    # power usage in VA
>     accumulatedEnergy:            int
>     timestamp:                    int    # time on Crownstone seconds since epoch with locale correction
>     dimmingAvailable:             bool   # dimming is available for use (it is not in the first 60 seconds after boot)
>     dimmingAllowed:               bool   # this Crownstone can dim
>     switchLocked:                 bool   # this Crownstone is switch-locked
>     hasError:                     bool   # this crownstone has an error, if the crownstone has an error, the errors: {} dict is only valid if errorMode: true. This boolean is always valid.
>     errorMode:                    bool   # summary type errorMode : the errors JSON is valid. This alternates with normal advertisements
>     errors: {
>         overCurrent:              bool
>         overCurrentDimmer:        bool
>         temperatureChip:          bool
>         temperatureDimmer:        bool
>         dimmerOnFailure:          bool
>         dimmerOffFailure:         bool
>         bitMask:                  int
>     }
>     timeIsSet:                    bool   # this crownstone knows what time it is
> }
>```

##### `UsbTopics.uartMessage`
> This topic will print anything you send to the USB dongle using Bluenet.uartEcho. This can be used for a ping-pong implementation.
> Data format is a dictionary with the fields shown below:
>```python
> {
>     data:             [array of ints]
>     string:           stringified representation of the data
> }
>```


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

#### `getCrownstoneIds()`
> Get a list of the CrownstoneIDs (ints) that are known to the library.

#### `stop()`
> Stop any running processes.

#### `isRunning()`
> Returns a Boolean indicating if the BluenetLib is running. This is relevant for the UART listener which communicates with the Crownstone USB.





# License

MIT

