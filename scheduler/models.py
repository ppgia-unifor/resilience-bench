from enum import Enum
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Workload:
    users: int
    rate: str
    duration: int

@dataclass(frozen=True)
class ClientSpec:
    strategy: str
    platform: str
    lib: str
    url: str
    pattern_config: dict
    

class FaultType(Enum):
    DELAY = "delay"
    ABORT = "abort"


@dataclass(frozen=True)
class Fault:
    fault_type: FaultType
    percentage: int
    duration: int
    status: int

@dataclass(frozen=True)
class Scenario:
    workload: Workload
    fault: Fault
    spec: ClientSpec


class Benchmark:
    rounds: int
    scenarios: List[Scenario] = []
