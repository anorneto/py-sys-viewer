from enum import Enum
from typing import Any, Dict, List
from dataclasses import dataclass, field
from helpers.constants import LIBREMONITOR_DLL_NAMESPACE


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
    Factor = "1"
    Power = "W"
    Data = "GB"
    SmallData = "MB"
    Throughput = "B/s"
    TimeSpan = "s"
    Energy = "mWh"
    Noise = "dBA"


@dataclass
class Sensor:
    index: int
    name: str
    identifier: str  # todo -> check this class
    type: str
    max: float | None
    min: float | None
    value: float | None

    @property
    def unit(self) -> str:
        return SensorTypeUnitEnum[self.type].value

    @property
    def value_with_unit(self) -> str:
        return f"{self.value} {self.unit}"

    @classmethod
    def from_libremonitor_sensor(cls, libremonitor_sensor) -> "Sensor":
        if (
            libremonitor_sensor.GetType().FullName
            != f"{LIBREMONITOR_DLL_NAMESPACE}.Hardware.Sensor"
        ):
            raise ValueError("Not a Sensor")

        sensor: Sensor = Sensor(
            index=libremonitor_sensor.Index,
            name=libremonitor_sensor.Name,
            identifier=str(libremonitor_sensor.Identifier),
            type=str(libremonitor_sensor.SensorType),
            max=libremonitor_sensor.Max,
            min=libremonitor_sensor.Min,
            value=libremonitor_sensor.Value,
        )

        return sensor

    def __repr__(self) -> str:
        return f"{self.index} | {self.name} - {self.value_with_unit}"
