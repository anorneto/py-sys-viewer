from .ilibremonitor import ILibreMonitorAdapter
from src.domain.dto import Hardware, HardwareType


class LibreHardwareAdapter(ILibreMonitorAdapter):
    @classmethod
    def from_libremonitor_hardware(cls, libremonitor_hardware) -> "Hardware":
        if type(libremonitor_hardware).__name__ != "IHardware":
            raise ValueError("Not a Hardware")

        hardware_type: HardwareType = HardwareType[
            str(libremonitor_hardware.HardwareType)
        ]

        hardware: Hardware = Hardware(
            identifier=str(libremonitor_hardware.Identifier),
            name=libremonitor_hardware.Name,
            type=hardware_type,
        )

        return hardware
