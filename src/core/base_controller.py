from dataclasses import dataclass
from typing import Any, List, Dict

from src.event import Event


@dataclass
class BaseController:
    """
    Base class for `controllers`, which perform transformations on sequence of `events`,
    returning another sequence of events.
    """

    @staticmethod
    def __call__(events: List[Event], **kwargs) -> List[Event]:
        raise NotImplementedError
