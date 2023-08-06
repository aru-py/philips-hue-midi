from typing import List, Dict

from src.core.base_controller import BaseController
from src.event import Event


class OutputController(BaseController):

    @staticmethod
    def __call__(events: List[Event], **kwargs) -> List[Event]:
        pass
        # todo implement
