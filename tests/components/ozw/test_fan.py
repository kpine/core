"""Test Z-Wave Lights."""
from homeassistant.components.ozw.fan import SPEED_TO_VALUE

from .common import setup_ozw


async def test_fan(hass, fan_data, fan_msg, sent_messages, caplog):
    """Test fan."""
    receive_message = await setup_ozw(hass, fixture=fan_data)

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


async def test_fan_ge12724(
    hass, ge12724_fan_data, fan_ge12730_msg, sent_messages, caplog
):
    """Test fan."""
    receive_message = await setup_ozw(hass, fixture=ge12724_fan_data)

    fan_msg = fan_ge12730_msg
    # Test loaded

    # Entity is a fan, not a light
    state = hass.states.get("light.in_wall_smart_fan_control_level")
    assert state is None

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
    assert msg["payload"] == {"Value": 0, "ValueIDKey": 407470097}

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
        "ValueIDKey": 407470097,
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
        "ValueIDKey": 407470097,
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
        "ValueIDKey": 407470097,
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
