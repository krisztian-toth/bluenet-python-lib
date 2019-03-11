from bluepy.btle import BTLEException

from BluenetLib.lib.protocol.Characteristics import CrownstoneCharacteristics
from BluenetLib.lib.protocol.ControlPackets import ControlPacketsGenerator
from BluenetLib.lib.protocol.Services import CSServices
from BluenetLib.lib.util.EncryptionHandler import EncryptionHandler


class ControlHandler:
    def __init__(self, bluetoothCore):
        self.core = bluetoothCore

    def getAndSetSessionNone(self):
        # read the nonce
        rawNonce = self.core.ble.readCharacteristicWithoutEncryption(
            CSServices.CrownstoneService,
            CrownstoneCharacteristics.SessionNonce)

        # decrypt it
        decryptedNonce = EncryptionHandler.decryptSessionNonce(rawNonce,
                                                               self.core.settings.guestKey)

        # load into the settings object
        self.core.settings.setSessionNonce(decryptedNonce)

    def setSwitchState(self, switchState):
        """
         :param switchState: number [0..1]
        """
        self._writeControlPacket(
            ControlPacketsGenerator.getSwitchStatePacket(switchState))

    def switchRelay(self, switchState):
        """
         :param switchState: number 0 is off, 1 is on.
        """
        self._writeControlPacket(
            ControlPacketsGenerator.getRelaySwitchPacket(switchState))

    def switchPWM(self, switchState):
        """
         :param switchState: number [0..1]
        """
        self._writeControlPacket(
            ControlPacketsGenerator.getPwmSwitchPacket(switchState))

    def commandFactoryReset(self):
        """
          If you have the keys, you can use this to put the crownstone back into factory default mode
        """
        self._writeControlPacket(
            ControlPacketsGenerator.getCommandFactoryResetPacket())

    def allowDimming(self, allow):
        """
        :param allow: bool
        """
        self._writeControlPacket(
            ControlPacketsGenerator.getAllowDimmingPacket(allow))

    def disconnect(self):
        """
          This forces the Crownstone to disconnect from you
        """
        try:
            self._writeControlPacket(
                ControlPacketsGenerator.getDisconnectPacket())
            self.core.ble.disconnect()
        except BTLEException as err:
            if err.code is BTLEException.DISCONNECTED:
                pass
            else:
                raise err

    def lockSwitch(self, lock):
        """
        :param lock: bool
        """
        self._writeControlPacket(
            ControlPacketsGenerator.getLockSwitchPacket(lock))

    def reset(self):
        self._writeControlPacket(ControlPacketsGenerator.getResetPacket())

    def setSchedulePacket(self, index, scheduleData):
        """
        Sets a new schedule task as per the specification defined at
        https://github.com/crownstone/bluenet/blob/master/docs/PROTOCOL.md#schedule-command-packet

        :param index: index of the entry
        :type index: int
        :param scheduleData: data required to build a schedule entry packet
        :type scheduleData: ScheduleData
        """
        dataByteArray = [index] + scheduleData.to_byte_array()
        self._writeControlPacket(
            ControlPacketsGenerator.getSetSchedulePacket(dataByteArray))

    """
    ---------------  UTIL  ---------------
    """

    def _readControlPacket(self, packet):
        return self.core.ble.readCharacteristic(CSServices.CrownstoneService,
                                                CrownstoneCharacteristics.Control)

    def _writeControlPacket(self, packet):
        self.core.ble.writeToCharacteristic(CSServices.CrownstoneService,
                                            CrownstoneCharacteristics.Control,
                                            packet)


class ScheduleData:
    """
    Data class for Schedule data required for a Schedule command packet as
    defined at
    https://github.com/crownstone/bluenet/blob/master/docs/PROTOCOL.md#schedule-command-packet
    """

    def __init__(self,
                 schedule_type,
                 trigger_timestamp,
                 repeat_data,
                 action_data,
                 override_mask=0):
        """
        For more details see the bluenet protocol specification at
        https://github.com/crownstone/bluenet/blob/master/docs/PROTOCOL.md#schedule-entry-packet

        :param schedule_type: combined repeat and action type
        :param trigger_timestamp: timestamp of the next time this entry
        triggers - set to 0 to remove this entry.
        :param repeat_data: repeat time data, depends on the repeat type.
        :param action_data: action data, depends on the action type.
        :param override_mask: bitmask of switch commands to override.
        """
        self.schedule_type = schedule_type
        self.trigger_timestamp = trigger_timestamp
        self.repeat_data = repeat_data
        self.action_data = action_data
        self.override_mask = override_mask

    def to_byte_array(self):
        return [0,
                self.schedule_type,
                self.override_mask,
                self.trigger_timestamp,
                self.repeat_data,
                self.action_data]
