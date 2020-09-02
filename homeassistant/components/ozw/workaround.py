"""Manufacturer specific workarounds."""
from enum import IntEnum

from openzwavemqtt.const import CommandClass, ValueIndex


class Manufacturer(IntEnum):
    """Manufacturer IDs."""

    GE_JASCO = 0x0063
    INOVELLI1 = 0x031E
    LEVITON = 0x001D


GE_FAN_CONTROLLER_14287_MULTILEVEL = (
    Manufacturer.GE_JASCO,
    0x4944,
    0x3034,
    1,
    CommandClass.SWITCH_MULTILEVEL,
    ValueIndex.SWITCH_MULTILEVEL_LEVEL,
)

INOVELLI_LZW36_FAN_LIGHT_MULTILEVEL = (
    Manufacturer.INOVELLI1,
    0x000E,
    0x0001,
    3,
    CommandClass.SWITCH_MULTILEVEL,
    ValueIndex.SWITCH_MULTILEVEL_LEVEL,
)

LEVITON_VRF01_1LZ_MULTILEVEL = (
    Manufacturer.LEVITON,
    0x1001,
    0x0334,
    1,
    CommandClass.SWITCH_MULTILEVEL,
    ValueIndex.SWITCH_MULTILEVEL_LEVEL,
)


# List of component workarounds
DEVICE_COMPONENT_MAPPING = {
    GE_FAN_CONTROLLER_14287_MULTILEVEL: "fan",
    INOVELLI_LZW36_FAN_LIGHT_MULTILEVEL: "fan",
    LEVITON_VRF01_1LZ_MULTILEVEL: "fan",
}


def get_device_component_mapping(value):
    """Get mapping of value to another component."""
    if not value.node.manufacturer_id.strip() or not value.node.product_type.strip():
        return None

    manufacturer_id = int(value.node_manufacturer_name, 16)
    product_type = int(value.node_product_type, 16)
    product_id = int(value.node_product_id, 16)

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
