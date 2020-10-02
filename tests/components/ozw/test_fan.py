"""Test Z-Wave Lights."""
from homeassistant.components.ozw.fan import SPEED_TO_VALUE

from .common import setup_ozw


async def test_fan(hass, fan_ge14287_data, fan_ge14287_msg, sent_messages, caplog):
    """Test fan."""
    receive_message = await setup_ozw(hass, fixture=fan_ge14287_data)

    # Test loaded
    state = hass.states.get("fan.in_wall_smart_fan_control_level")
    assert state is not None
    assert state.state == "on"

    # Test turning off
    await hass.services.async_call(
        "fan",
        "turn_off",
        {"entity_id": "fan.in_wall_smart_fan_control_level"},
        blocking=True,
    )

    assert len(sent_messages) == 1
    msg = sent_messages[-1]
    assert msg["topic"] == "OpenZWave/1/command/setvalue/"
    assert msg["payload"] == {"Value": 0, "ValueIDKey": 172589073}

    fan_msg = fan_ge14287_msg

    # Feedback on state
    fan_msg.decode()
    fan_msg.payload["Value"] = 0
    fan_msg.encode()
    receive_message(fan_msg)
    await hass.async_block_till_done()

    state = hass.states.get("fan.in_wall_smart_fan_control_level")
    assert state is not None
    assert state.state == "off"

    # Test turning on
    new_speed = "medium"
    await hass.services.async_call(
        "fan",
        "turn_on",
        {"entity_id": "fan.in_wall_smart_fan_control_level", "speed": new_speed},
        blocking=True,
    )

    assert len(sent_messages) == 2
    msg = sent_messages[-1]
    assert msg["topic"] == "OpenZWave/1/command/setvalue/"
    assert msg["payload"] == {
        "Value": SPEED_TO_VALUE[new_speed],
        "ValueIDKey": 172589073,
    }

    # Feedback on state
    fan_msg.decode()
    fan_msg.payload["Value"] = SPEED_TO_VALUE[new_speed]
    fan_msg.encode()
    receive_message(fan_msg)
    await hass.async_block_till_done()

    state = hass.states.get("fan.in_wall_smart_fan_control_level")
    assert state is not None
    assert state.state == "on"
    assert state.attributes["speed"] == new_speed

    # Test turn on without speed
    await hass.services.async_call(
        "fan",
        "turn_on",
        {"entity_id": "fan.in_wall_smart_fan_control_level"},
        blocking=True,
    )

    assert len(sent_messages) == 3
    msg = sent_messages[-1]
    assert msg["topic"] == "OpenZWave/1/command/setvalue/"
    assert msg["payload"] == {
        "Value": 255,
        "ValueIDKey": 172589073,
    }

    # Feedback on state
    fan_msg.decode()
    fan_msg.payload["Value"] = SPEED_TO_VALUE[new_speed]
    fan_msg.encode()
    receive_message(fan_msg)
    await hass.async_block_till_done()

    state = hass.states.get("fan.in_wall_smart_fan_control_level")
    assert state is not None
    assert state.state == "on"
    assert state.attributes["speed"] == new_speed

    # Test set speed to off
    new_speed = "off"
    await hass.services.async_call(
        "fan",
        "set_speed",
        {"entity_id": "fan.in_wall_smart_fan_control_level", "speed": new_speed},
        blocking=True,
    )

    assert len(sent_messages) == 4
    msg = sent_messages[-1]
    assert msg["topic"] == "OpenZWave/1/command/setvalue/"
    assert msg["payload"] == {
        "Value": SPEED_TO_VALUE[new_speed],
        "ValueIDKey": 172589073,
    }

    # Feedback on state
    fan_msg.decode()
    fan_msg.payload["Value"] = SPEED_TO_VALUE[new_speed]
    fan_msg.encode()
    receive_message(fan_msg)
    await hass.async_block_till_done()

    state = hass.states.get("fan.in_wall_smart_fan_control_level")
    assert state is not None
    assert state.state == "off"

    # Test invalid speed
    new_speed = "invalid"
    await hass.services.async_call(
        "fan",
        "set_speed",
        {"entity_id": "fan.in_wall_smart_fan_control_level", "speed": new_speed},
        blocking=True,
    )

    assert len(sent_messages) == 4
    assert "Invalid speed received: invalid" in caplog.text


async def test_fan_ge_12724_workaround(hass, ge12724_fan_data):
    """Test GE 12724 fan workaround."""
    await setup_ozw(hass, fixture=ge12724_fan_data)

    # Test loaded

    # Entity is a fan, not a light
    state = hass.states.get("light.in_wall_smart_fan_control_level")
    assert state is None

    state = hass.states.get("fan.in_wall_smart_fan_control_level")
    assert state is not None


async def test_fan_leviton_vfr01_1lz_workaround(hass, fan_leviton_vfr01_1lz_data):
    """Test GE 12724 fan workaround."""
    await setup_ozw(hass, fixture=fan_leviton_vfr01_1lz_data)

    # Test loaded

    # Entity is a fan, not a light
    state = hass.states.get("light.living_room_fan_level")
    assert state is None

    state = hass.states.get("fan.living_room_fan_level")
    assert state is not None


async def test_fan_inovelli_lzw36_workaround(hass, fan_lzw36_data):
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
