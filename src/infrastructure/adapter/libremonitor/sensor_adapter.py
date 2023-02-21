from .ilibremonitor import ILibreMonitorAdapter
from src.domain.dto import Sensor, SensorTypeUnitEnum


class LibreSensorAdapter(ILibreMonitorAdapter):
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
