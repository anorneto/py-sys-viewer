from typing import List
from dataclasses import dataclass, field
from .sensor import Sensor
from src.common.constants import GlobalConstants
from enum import StrEnum, auto


class HardwareType(StrEnum):
    Motherboard = auto()
    SuperIO = auto()
    Cpu = auto()
    Memory = auto()
    GpuNvidia = auto()
    GpuAmd = auto()
    GpuIntel = auto()
    Storage = auto()
    Network = auto()
    Cooler = auto()
    EmbeddedController = auto()
    Psu = auto()
    Battery = auto()


@dataclass
class Hardware:
    identifier: str  # todo -> check this class
    name: str
    type: HardwareType
    sub_hardware: List["Hardware"] = field(default_factory=list)
    sensors: List[Sensor] = field(default_factory=list)

    def __post_init__(self):
        if self.sub_hardware is None:
            self.sub_hardware = []
        if self.sensors is None:
            self.sensors = []

    def __repr__(self) -> str:
        return f"> {self.name} - {self.type}"
