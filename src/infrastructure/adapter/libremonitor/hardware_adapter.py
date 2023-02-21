from typing import List
from .ilibremonitor import ILibreMonitorAdapter
from src.domain.dto import Hardware, HardwareType, Sensor
from .sensor_adapter import LibreSensorAdapter


class LibreHardwareAdapter(ILibreMonitorAdapter):
    @classmethod
    def from_libremonitor_hardware(cls, libremonitor_hardware) -> "Hardware":
        if type(libremonitor_hardware).__name__ != "IHardware":
            raise ValueError("Not a Hardware")

        hardware_type: HardwareType = HardwareType[
            str(libremonitor_hardware.HardwareType)
        ]

        libremonitor_sensor_list = (
            libremonitor_sensor
            for libremonitor_sensor in libremonitor_hardware.Sensors
            if libremonitor_sensor.Value is not None
        )
        sensor_list: List[Sensor] = []
        for libremonitor_sensor in libremonitor_sensor_list:
            sensor: Sensor = LibreSensorAdapter.from_libremonitor_sensor(
                libremonitor_sensor=libremonitor_sensor
            )
            sensor_list.append(sensor)

        hardware: Hardware = Hardware(
            identifier=str(libremonitor_hardware.Identifier),
            name=libremonitor_hardware.Name,
            type=hardware_type,
            sensors=sensor_list,
        )

        return hardware
