"""Manufacturer specific workarounds."""
from enum import IntEnum

from openzwavemqtt.const import CommandClass, ValueIndex
from openzwavemqtt.models.value import OZWValue


class Manufacturer(IntEnum):
    """Manufacturer IDs."""

    GE_JASCO = 0x0063
    INOVELLI = 0x031E
    LEVITON = 0x001D


# This fan controller is pre-Z-Wave Plus so it identifies as a multilevel switch.
GE_FAN_CONTROLLER_14287_MULTILEVEL = (
    (
        Manufacturer.GE_JASCO,
        0x4944,
        0x3034,
        1,
        CommandClass.SWITCH_MULTILEVEL,
        ValueIndex.SWITCH_MULTILEVEL_LEVEL,
    ),
    "fan",
)

# This fan/light combo switch is Z-Wave Plus V2 so it identifies as a multilevel switch.
# It is a multi-channel device and endpoint 2 (OZW instance 3) is the fan switch.
INOVELLI_LZW36_FAN_LIGHT_MULTILEVEL = (
    (
        Manufacturer.INOVELLI,
        0x000E,
        0x0001,
        3,
        CommandClass.SWITCH_MULTILEVEL,
        ValueIndex.SWITCH_MULTILEVEL_LEVEL,
    ),
    "fan",
)

# This fan controller is pre-Z-Wave Plus so it identifies as a multilevel switch.
LEVITON_VRF01_1LZ_MULTILEVEL = (
    (
        Manufacturer.LEVITON,
        0x1001,
        0x0334,
        1,
        CommandClass.SWITCH_MULTILEVEL,
        ValueIndex.SWITCH_MULTILEVEL_LEVEL,
    ),
    "fan",
)

DEVICE_COMPONENT_MAPPING = dict(
    (
        GE_FAN_CONTROLLER_14287_MULTILEVEL,
        INOVELLI_LZW36_FAN_LIGHT_MULTILEVEL,
        LEVITON_VRF01_1LZ_MULTILEVEL,
    )
)


def get_device_component_mapping(value: OZWValue):
    """Get the mapping of a value to another component."""
    try:
        manufacturer_id = int(value.node.node_manufacturer_id, 16)
        product_type = int(value.node.node_product_type, 16)
        product_id = int(value.node.node_product_id, 16)
    except ValueError:
        return None

    return DEVICE_COMPONENT_MAPPING.get(
        (
            manufacturer_id,
            product_type,
            product_id,
            value.instance,
            value.command_class,
            value.index,
        )
    )
