from enum import Enum


class ProtocolType(Enum):
    RADIO_433MHz = "RADIO_433MHz"
    ZIGBEE = "ZIGBEE"


class ButtonType(Enum):
    BUTTON = "button"
