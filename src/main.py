import clr  # package pythonnet, not clr
from typing import List

from src.domain.use_case.get_hardware_data import GetHardwareData
from .domain.dto import Sensor, Hardware
from .infrastructure.repositories.hardware_monitor_repository import (
    LibreHardwareMonitorRepository,
)

import time
from .presenters.cli.cli_app import CliApp


if __name__ == "__main__":
    app = CliApp()
    app.run()
    # print("\nCPUMonitor:")
    # CPUHandle = initialize_cputhermometer()
    # fetch_stats(CPUHandle)
