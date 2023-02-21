import clr
from typing import List
from logging import Logger
from structlog import get_logger
from src.infrastructure.adapter.libremonitor import LibreHardwareAdapter

from src.common.constants import DLLS_FILE_LOCATION_DICT

from src.domain.dto import Hardware, Sensor

from typing import List


class LibreHardwareMonitorRepository:
    _libre_handler: object | None = None

    def __init__(
        self,
        logger: Logger | None = None,
        motherboard_enabled: bool = False,
        memory_enabled: bool = False,
        controller_enabled: bool = False,
        network_enabled: bool = False,
        storage_enabled: bool = False,
    ) -> None:
        self.logger = logger or get_logger(__file__)
        self.init_librehardwaremonitor(
            motherboard_enabled=motherboard_enabled,
            memory_enabled=memory_enabled,
            controller_enabled=controller_enabled,
            network_enabled=network_enabled,
            storage_enabled=storage_enabled,
        )

    @classmethod
    def init_librehardwaremonitor(
        cls,
        motherboard_enabled: bool = False,
        memory_enabled: bool = False,
        controller_enabled: bool = False,
        network_enabled: bool = False,
        storage_enabled: bool = False,
    ) -> None:
        for key, value in DLLS_FILE_LOCATION_DICT.items():
            clr.AddReference(value)

        from LibreHardwareMonitor import Hardware  # noqa

        handler = Hardware.Computer()
        handler.IsCpuEnabled = True
        handler.IsGpuEnabled = True

        # Optional
        handler.IsMotherboardEnabled = motherboard_enabled
        handler.IsMemoryEnabled = memory_enabled
        handler.IsStorageEnabled = storage_enabled
        handler.IsControllerEnabled = controller_enabled
        handler.IsNetworkEnabled = network_enabled
        handler.Open()

        cls._libre_handler = handler

    def fetch_all_data(self) -> List[Hardware]:
        hardware_list: List[Hardware] = []
        for libre_hardware in self._libre_handler.Hardware:  # type: ignore
            libre_hardware.Update()
            hardware: Hardware = LibreHardwareAdapter.from_libremonitor_hardware(
                libre_hardware
            )
            sub_hardware_list: List[Hardware] = []
            for libre_sub_hardware in libre_hardware.SubHardware:
                libre_sub_hardware.Update()
                sub_hardware: Hardware = (
                    LibreHardwareAdapter.from_libremonitor_hardware(libre_sub_hardware)
                )
                sub_hardware_list.append(sub_hardware)
            hardware.sub_hardware = sub_hardware_list
            hardware_list.append(hardware)

        return hardware_list
