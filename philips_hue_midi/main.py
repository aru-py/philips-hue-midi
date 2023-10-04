"""
main.py
"""

import asyncio
import atexit
import logging
import mido
import time
from logging import getLogger
from mido import Message
from phue import Bridge
from typing import List

from .config import config
from .constants import LEFT_PEDAL
from .controllers.note_controller import NoteController
from .core.channel import Channel
from .event import Event
from .utils import save_lights_state, create_channels

logger = getLogger()
logger.setLevel(logging.DEBUG)

# connect to hue lights
bridge = Bridge(config.bridge_ip)
bridge.connect()

state = save_lights_state(bridge)


def restore_lights():
    for light_id, light_state in state.items():
        bridge.set_light(light_id, light_state)


# restore original configuration after program quits
atexit.register(restore_lights)
channels = create_channels(bridge, config)

# turn on lights for master channel
bridge.set_light(channels[0].lights, {
    'on': True,
    'bri': 1
})

# start timer
running = True

# event queues
key_down_events: List[Event] = []
key_up_events: List[Event] = []


def add_to_queue(e: Message):
    # todo support control changes

    global running
    if e.type == 'control_change':
        if e.control == LEFT_PEDAL and e.value == 127:  # todo max
            running = not running
            if not running:
                bridge.set_light(channels[0].lights, 'on', False)
            else:
                for light_num in channels[0].lights:
                    bridge.set_light(light_num, 'on', True)
                    time.sleep(.1)
        return

    event = Event(note=e.note, velocity=e.velocity, type=e.type)

    logger.warning(event)  # log events todo not warning..

    if event.is_on():
        key_down_events.insert(0, event)
    else:
        key_up_events.insert(0, event)


async def event_loop(key_down_events, key_up_events):
    # todo check event queue for sequences?
    # todo auto create default channels

    channel_events = NoteController.__call__(key_down_events)

    wait_for = []

    # todo make dict?
    # todo explanations
    for idx, event in enumerate(reversed(channel_events)):
        if event:
            channel_idx = len(channel_events) - idx
            wait_for.append(channels[channel_idx](event))

    for item in wait_for:
        await item

    wait_for = []

    for event in key_up_events:
        wait_for.append(channels[1](event))

    for item in wait_for:
        await item

    # clear buffers
    Channel.clear_locks()


async def main():
    global key_down_events, key_up_events
    sample_rate = 60
    while True:
        time.sleep(sample_rate / 1000)
        if running:
            await event_loop(key_down_events, key_up_events)
        key_down_events = []
        key_up_events = []


# connect to keyboard
port = mido.open_input()
logger.warning(f"Connected to midi input {port.name}")
port.callback = add_to_queue

if __name__ == '__main__':
    asyncio.run(main())
