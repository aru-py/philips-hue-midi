import toml
from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class Config:
    """
    Configuration schema (used for validation).
    # todo better way?
    """
    palette: List[str]
    bridge_ip: str
    channels: Any


with open('config.toml', 'r') as f:
    config = Config(**toml.load(f))
