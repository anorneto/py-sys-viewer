import clr  # package pythonnet, not clr
from typing import List
from .domain.dto import Sensor, Hardware
from .infrastructure.repositories.hardware_monitor_repository import (
    LibreHardwareMonitorRepository,
)

import time

if __name__ == "__main__":
    while True:
        print("LibreHardwareMonitor:")
        repository = LibreHardwareMonitorRepository()
        hardware_list: List[Hardware] = repository.fetch_all_data()

        for hardware in hardware_list:
            print(hardware)
            for sensor in hardware.sensors:
                print(f"    >{sensor}")
            else:
                for sub_hardware in hardware.sub_hardware:
                    print(f"* {sub_hardware}")
                    for sensor in sub_hardware.sensors:
                        print(f"    >{sensor}")

        time.sleep(2)
    # print("\nCPUMonitor:")
    # CPUHandle = initialize_cputhermometer()
    # fetch_stats(CPUHandle)
