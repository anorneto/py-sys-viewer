from enum import Enum
from typing import Any, Dict, List
from dataclasses import dataclass, field
from common.constants import GlobalConstants


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

    @classmethod
    def from_libremonitor_sensor(cls, libremonitor_sensor) -> "Sensor":
        if type(libremonitor_sensor).__name__ != f"ISensor":
            raise ValueError("Not a Sensor")

        sensor_type: SensorTypeUnitEnum = SensorTypeUnitEnum[
            str(libremonitor_sensor.SensorType)
        ]

        sensor: Sensor = Sensor(
            identifier=str(libremonitor_sensor.Identifier),
            index=libremonitor_sensor.Index,
            name=libremonitor_sensor.Name,
            type=sensor_type,
            max=libremonitor_sensor.Max,
            min=libremonitor_sensor.Min,
            value=libremonitor_sensor.Value,
        )

        return sensor

    def __repr__(self) -> str:
        return f"{self.type.name} | {self.index} | {self.name} - {self.value_with_unit}"
