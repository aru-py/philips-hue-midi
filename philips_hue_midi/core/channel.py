import math
from dataclasses import dataclass, field
from random import random
from typing import List, Dict

from phue import Bridge

from ..event import Event


def interpolate(p, color_range):
    """
    Takes in `color_range`, a pair of tuples and interpolates linearly
    at the point `p`.
    """
    x = (color_range[1][0] - color_range[0][0]) * p + color_range[0][0]
    y = (color_range[1][1] - color_range[0][1]) * p + color_range[0][1]
    return x, y


def get_default_brightness_settings() -> Dict[str, int]:
    # todo move these to constants file
    return {"off_min": 0, "on_min": 10, "entropy": 20, "sensitivity": 12}


def get_default_transition_settings() -> Dict[str, int]:
    return {"min": 21}


@dataclass
class Channel:
    """
    Channel maps events to lights.
    """

    bridge: Bridge
    lights: List
    colors: List
    brightness: Dict[str, int] = field(default_factory=get_default_brightness_settings)
    transition: Dict[str, int] = field(default_factory=get_default_transition_settings)

    # maps notes to lights todo fix event queue...?

    # todo rename
    light_states = {}
    lights_locked = set()

    async def __call__(self, event: Event):
        return self._process_keydown(event) if event.is_on() else self._process_keyup(event)

    @classmethod
    def clear_locks(cls):
        cls.lights_locked.clear()

    def _process_keydown(self, event: Event):
        for light_num in self.lights:
            if light_num in Channel.lights_locked:
                continue

            self.bridge.set_light(light_num, {
                'xy': [*interpolate(((max(40, min(event.note, 80))) - 40) / 40, self.colors)],
                'bri': round(self.brightness['on_min'] + (random() * self.brightness['entropy']) - self.brightness[
                    'entropy'] / 2 + math.sqrt(event.velocity) * self.brightness['sensitivity']),
                'transitiontime': max(5, round(-event.velocity / 4 + self.transition['min'])),
            })

            Channel.light_states[light_num] = event.note
            Channel.lights_locked.add(light_num)

    def _process_keyup(self, event: Event):
        # todo optimize this algorithm

        to_remove = []
        for light_num, note in Channel.light_states.items():
            if note == event.note:
                velocity = event.velocity
                self.bridge.set_light(light_num, {
                    'bri': self.brightness['off_min'],
                    'transitiontime': max(5, round(-velocity / 4 + self.transition['min']))
                })
                to_remove.append(light_num)

        for light_num in to_remove:
            Channel.light_states.pop(light_num)
