from dataclasses import dataclass


@dataclass
class Event:
    """
    Represents a piano event.
    """
    note: int  # represents note pitch (27 - 108, inclusive)
    type: str  # note_on, note_off, or pedal event
    velocity: int  # represents speed of key-press (0 - 127, inclusive)

    def is_key_event(self):
        return self.type == 'note_on' or self.type == 'note_off'

    def is_on(self):
        return self.type == 'note_on'

    def is_off(self):
        return self.type == 'note_off'
