"""
register_controller.py

NOTE: THIS IS NOT USED


"""


from typing import List

from ..core.base_controller import BaseController
from ..event import Event


# todo make generic
class RegisterController(BaseController):

    @staticmethod
    def __call__(events: List[Event], **kwargs) -> List[Event]:

        # todo move constants
        thresholds = {"bass": 21, "mid": 48, "treble": 83}
        bass, mid, treble = [], [], []

        # todo rearrange
        for event in events:
            if event.note >= thresholds['treble']:
                treble = [event]
            elif event.note >= thresholds['mid']:
                mid = [event]
            elif event.note >= thresholds['bass']:
                bass = [event]

        return [*mid, *bass, *treble]
