from enum import Enum
from typing import Any, Dict, List
from dataclasses import dataclass, field
from src.common.constants import GlobalConstants


class SensorTypeUnitEnum(Enum):
    Voltage = "V"
    Clock = "MHz"
    Temperature = "\u00B0C"
    Load = "%"
    Frequency = "Hz"
    Fan = "RPM"
    Flow = "L/h"
    Control = "%"
    Level = "%"
    Factor = "* 1"
    Power = "W"
    Data = "GB"
    SmallData = "MB"
    Throughput = "B/s"
    TimeSpan = "s"
    Energy = "mWh"
    Noise = "dBA"


@dataclass
class Sensor:
    identifier: str  # todo -> check this class
    index: int
    name: str
    type: SensorTypeUnitEnum
    max: float | None
    min: float | None
    value: float | None

    @property
    def unit(self) -> str:
        return self.type.value

    @property
    def value_with_unit(self) -> str:
        return f"{self.value} {self.unit}"

    def __repr__(self) -> str:
        return f"{self.type.name} | {self.index} | {self.name} - {self.value_with_unit}"
