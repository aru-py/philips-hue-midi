"""
main.py
"""

import asyncio
import atexit
import logging
import time
from logging import getLogger
from typing import List

import mido
from mido import Message
from phue import Bridge

from philips_hue_midi import constants
from .config import config
from .constants import LEFT_PEDAL
from .controllers.note_controller import NoteController
from .core.channel import Channel
from .event import Event
from .utils import save_lights_state, create_channels

logger = getLogger()
logger.setLevel(logging.DEBUG)

# connect to Hue lights
bridge = Bridge(config.bridge_ip)
bridge.connect()

state = save_lights_state(bridge)


# todo this should be moved into utils
def restore_lights():
    for light_id, light_state in state.items():
        bridge.set_light(light_id, light_state)


# restore original configuration when program is exited
atexit.register(restore_lights)

channels = create_channels(bridge, config)

# turn on lights for master channel
bridge.set_light(channels[0].lights, {"on": True, "bri": 1})

# start timer
running = True

# event queues
key_down_events: List[Event] = []
key_up_events: List[Event] = []


def add_to_queue(event: Message):
    # todo support control changes

    global running
    if event.type == "control_change":
        if event.control == LEFT_PEDAL and event.value == 127:  # todo max
            running = not running
            if not running:
                bridge.set_light(channels[0].lights, "on", False)
            else:
                for light_num in channels[0].lights:
                    bridge.set_light(light_num, "on", True)
                    time.sleep(0.1)
        return

    event = Event(note=event.note, velocity=event.velocity, type=event.type)
    logger.warning(event)  # log events

    if event.is_on():
        key_down_events.insert(0, event)
    else:
        key_up_events.insert(0, event)


async def event_loop(key_down_events, key_up_events):
    # todo check event queue for sequences?
    # todo auto create default channels

    # map keydown events to channel events
    channel_events = NoteController.__call__(key_down_events)

    wait_for = []

    # todo make dict?
    # todo explanations
    for idx, event in enumerate(reversed(channel_events)):
        if event:
            channel_idx = len(channel_events) - idx
            try:
                wait_for.append(channels[channel_idx](event))
            except KeyError:
                # use master channel if no channel exists
                logger.warning(f"MISSING CHANNEL {channel_idx}. Using master fallback.")
                wait_for.append(channels[0](event))

    for item in wait_for:
        await item

    wait_for = []

    for event in key_up_events:
        wait_for.append(channels[0](event))

    for item in wait_for:
        await item

    # clear buffers
    Channel.clear_locks()


async def main():
    print("Starting program!")
    global key_down_events, key_up_events
    while True:
        time.sleep(constants.SAMPLE_RATE / 1000)
        if running:
            await event_loop(key_down_events, key_up_events)
        key_down_events = []
        key_up_events = []

def run():
    asyncio.run(main())

# connect to keyboard
port = mido.open_input()
logger.warning(f"Connected to midi input {port.name}")
port.callback = add_to_queue

if __name__ == "__main__":
    run()
