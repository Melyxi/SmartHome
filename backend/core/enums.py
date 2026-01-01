from enum import Enum, StrEnum


class ProtocolType(StrEnum):
    RADIO_433MHz = "RADIO_433MHz"
    ZIGBEE = "ZIGBEE"
    MODULE = "MODULE"


class ButtonType(Enum):
    BUTTON = "button"
