import toml
from dataclasses import dataclass
from typing import Dict, Any, List
import sys


@dataclass
class Config:
    """
    Configuration schema (used for validation).
    # todo better way?
    """
    palette: List[str]
    bridge_ip: str
    channels: Any


with open(sys.argv[1], 'r') as f:
    config = Config(**toml.load(f))
