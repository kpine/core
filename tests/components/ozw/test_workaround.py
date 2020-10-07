"""Test Z-Wave workarounds."""
from .common import setup_ozw


async def test_workaround_ge_12724_fan(hass, ge12724_fan_data):
    """Test GE 12724 fan workaround."""
    await setup_ozw(hass, fixture=ge12724_fan_data)

    # Test loaded

    state = hass.states.get("light.in_wall_smart_fan_control_level")
    assert state is None

    state = hass.states.get("fan.in_wall_smart_fan_control_level")
    assert state is not None


async def test_workaround_leviton_vfr01_1lz_fan(hass, fan_leviton_vfr01_1lz_data):
    """Test GE 12724 fan workaround."""
    await setup_ozw(hass, fixture=fan_leviton_vfr01_1lz_data)

    # Test loaded

    state = hass.states.get("light.living_room_fan_level")
    assert state is None

    state = hass.states.get("fan.living_room_fan_level")
    assert state is not None


async def test_workaround_inovelli_lzw36_fan(hass, fan_lzw36_data):
    """Test GE 12724 fan workaround."""
    await setup_ozw(hass, fixture=fan_lzw36_data)

    # Test loaded

    # This device has 3 endpoints/instances:
    #  1. Root device
    #  2. Light dimmer
    #  3. Fan controller

    state = hass.states.get("light.kids_room_switch_instance_1_level")
    assert state is not None

    state = hass.states.get("light.kids_room_switch_instance_2_level")
    assert state is not None

    state = hass.states.get("fan.kids_room_switch_instance_3_level")
    assert state is not None
