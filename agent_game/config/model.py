from dataclasses import dataclass, field
from typing import List

@dataclass
class AgentConfig:
    agent_type: str = "Basic"
    occupance_size: int = 0
    nn_layers: List[int] = field(default_factory=lambda: [64])
    lr: float = 0.001
    gamma: float = 0.9
    batch_size: int = 1000
    max_memory: int = 10000

def config_from_dict(d: dict) -> AgentConfig:
    return AgentConfig(**d)

def dict_from_config(cfg: AgentConfig) -> dict:
    return cfg.__dict__
