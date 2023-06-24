from enum import Enum


class Workload:
    users: int
    rate: str
    duration: int


class ClientSpec:
    strategy: str
    platform: str
    lib: str
    url: str
    pattern_config: dict
    

class FaultType(Enum):
    DELAY = 1
    ABORT = 2


class Fault:
    faultType: FaultType
    percentage: int
    duration: int


