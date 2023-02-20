from random import random
from typing import Any, List
from dataclasses import dataclass

from phue import Bridge

from event import Event
from utils import interpolate


# todo support for "sub-channels"

@dataclass
class Channel:
    """
    Channel is the interface between events and lights.
    """

    bridge: Bridge
    lights: List

    color_range: List
    entropy: int
    transition_time_min: int
    brightness_off_min: int
    brightness_on_min: int

    key_locks = {}

    def process_event(self, event: Event):
        return self._process_keydown(event) if event.is_on() else self._process_keyup(event)

    def _process_keydown(self, event: Event):
        note = event.note

        if note in Channel.key_locks:
            Channel.key_locks.pop(note)

        velocity = event.velocity
        for light in self.lights:
            self.bridge.set_light(light, {
                'xy': [*interpolate((note - 21) / 108, self.color_range)],
                'bri': self.brightness_on_min + round(random() * self.entropy),
                'transitiontime': max(5, round(-velocity / 4 + self.transition_time_min)),
            })

        Channel.key_locks[note] = self.lights
        return True

    def _process_keyup(self, event: Event):
        note = event.note
        if lights := Channel.key_locks.get(note):
            velocity = event.velocity
            self.bridge.set_light(lights, {
                'bri': self.brightness_off_min,
                'transitiontime': max(5, round(-velocity / 4 + self.transition_time_min))
            })
            Channel.key_locks.pop(note)
            return True
        return False
