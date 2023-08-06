from dataclasses import dataclass


@dataclass
class Event:

    note: int
    type: str
    velocity: int

    def is_key_event(self):
        return self.type == 'note_on' or self.type == 'note_off'

    def is_on(self):
        return self.type == 'note_on'

    def is_off(self):
        return not self.is_on()
