# bluenet-python-lib

Official Python lib for Crownstone. 

This library has two different ways to interact with Crownstones.
- Communication over serial with a "Crownstone Unified System Bridge", or **Crownstone USB**. Works on all platforms.
    - USB library documentation can be found in [README_USB](https://github.com/crownstone/bluenet-python-lib/blob/master/README_USB.MD)
- Bluetooth via BlueZ. This only works on linux.
    - Bluetooth library documentation can be found in [README_BLE](https://github.com/crownstone/bluenet-python-lib/blob/master/README_BLE.MD)

The first method works with additional hardware that you plug into a USB port on your hub / gateway / computer / laptop. This is in the form-factor of a USB stick and can be bought at the [shop](https://shop.crownstone.rocks/products/crownstone-usb-dongle).

The second method uses the BLE chip on your hub / gateway / computer / laptop and does not need additional hardware. It requires so-called Bluez libraries. 

# Pros & Cons

The USB stick has an nRF52 on-board. This means it hooks up directly into the Crownstone mesh. It also works for platforms where the Bluez library is not so reliable (e.g. a Raspberry PI). However, it has as disadvantage that you need a USB port and that you need to buy the dongle. 

# License

MIT

