"""
router.py

NOTE: THIS IS NOT USED
"""

from typing import List

from ..core.base_controller import BaseController
from ..event import Event


class OutputController(BaseController):
    @staticmethod
    def __call__(events: List[Event], **kwargs) -> List[Event]:
        pass
        # todo implement
