from typing import List
from src.infrastructure.repositories.hardware_monitor_repository import (
    LibreHardwareMonitorRepository,
)
from src.domain.dto.hardware import Hardware

from src.common.helpers.logging import get_logger, Logger


class GetHardwareData:
    def __init__(
        self,
        hardware_repo: LibreHardwareMonitorRepository | None = None,
        logger: Logger | None = None,
    ) -> None:
        self._hardware_repo = hardware_repo or LibreHardwareMonitorRepository(
            logger=logger,
            motherboard_enabled=True,
        )
        self._logger = logger or get_logger(__name__)

    def execute(self) -> List[Hardware]:
        hardware_list: List[Hardware] = self._hardware_repo.fetch_all_data()

        return hardware_list
