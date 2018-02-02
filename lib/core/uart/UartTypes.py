from enum import IntEnum

class TxOpcode(IntEnum):
	CONTROL =                          1

	ENABLE_ADVERTISEMENT =             10000
	ENABLE_MESH =                      10001

	ADC_CONFIG_GET =                   10100
	ADC_CONFIG_SET =                   10101
	ADC_CONFIG_SET_RANGE =             10102
	ADC_CONFIG_INC_RANGE_CURRENT =     10103
	ADC_CONFIG_DEC_RANGE_CURRENT =     10104
	ADC_CONFIG_INC_RANGE_VOLTAGE =     10105
	ADC_CONFIG_DEC_RANGE_VOLTAGE =     10106
	ADC_CONFIG_DIFFERENTIAL_CURRENT =  10108
	ADC_CONFIG_DIFFERENTIAL_VOLTAGE =  10109
	ADC_CONFIG_VOLTAGE_PIN =           10110

	POWER_LOG_CURRENT =                10200
	POWER_LOG_VOLTAGE =                10201
	POWER_LOG_FILTERED_CURRENT =       10202
	POWER_LOG_FILTERED_VOLTAGE =       10203
	POWER_LOG_POWER =                  10204

class RxOpcode(IntEnum):
	ACK =                              0
	POWER_SAMPLES =                    4
	MESH_STATE_0 =                     100   # For 1st handle, next handle has opcode of 1 larger.
	MESH_STATE_1 =                     101   # Second state handle
	MESH_STATE_LAST =                  101   # Last state handle

	ADC_CONFIG =                       10100

	POWER_LOG_CURRENT =                10200
	POWER_LOG_VOLTAGE =                10201
	POWER_LOG_FILTERED_CURRENT =       10202
	POWER_LOG_FILTERED_VOLTAGE =       10203
	POWER_LOG_POWER =                  10204