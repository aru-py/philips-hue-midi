from typing import List, Dict

from ..core.base_controller import BaseController
from ..event import Event


class OutputController(BaseController):

    @staticmethod
    def __call__(events: List[Event], **kwargs) -> List[Event]:
        pass
        # todo implement
