"""
note_controller.py
"""

from typing import List, Union

from ..core.base_controller import BaseController
from ..event import Event


class NoteController(BaseController):
    """
    Note controller maps
    """

    @classmethod
    def __call__(cls, events: List[Union[None, Event]], **kwargs) -> List[Union[None, Event]]:
        res = [None] * 12
        for event in sorted(filter(None, events), key=lambda e: e.note):
            # returns 0 - 11 (representing the pitch class of note)
            pitch_class = (event.note - 12) % 12
            res[pitch_class] = event
        return res
