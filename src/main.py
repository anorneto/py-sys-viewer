import clr  # package pythonnet, not clr

from .domain.dto import Sensor, Hardware
from .common.constants import DLLS_FILE_LOCATION_DICT


def initialize_librehardwaremonitor():
    for key, value in DLLS_FILE_LOCATION_DICT.items():
        clr.AddReference(value)

    from LibreHardwareMonitor import Hardware  # noqa

    handle = Hardware.Computer()
    handle.IsMotherboardEnabled = True
    handle.IsCpuEnabled = True
    # handle.IsGpuEnabled = True
    # handle.IsMemoryEnabled = True
    # handle.IsControllerEnabled = True
    # handle.IsNetworkEnabled = True
    # handle.IsStorageEnabled = True
    handle.Open()
    return handle


def fetch_stats(handle):
    for hardware in handle.Hardware:
        hardware.Update()
        print(Hardware.from_libremonitor_hardware(hardware))
        for sensor in hardware.Sensors:
            parse_sensor(sensor)
        for sub_hardware in hardware.SubHardware:
            sub_hardware.Update()
            print(Hardware.from_libremonitor_hardware(sub_hardware))
            for subsensor in sub_hardware.Sensors:
                parse_sensor(subsensor)


def parse_sensor(sensor):
    print(Sensor.from_libremonitor_sensor(sensor))
    return
    if sensor.Value is not None:
        if type(sensor).__module__ == "LibreHardwareMonitor.Hardware":
            sensortypes = openhardwaremonitor_sensortypes
            hardwaretypes = openhardwaremonitor_hwtypes
        else:
            return

        if sensor.SensorType == sensortypes.index("Temperature"):
            print(
                "%s %s Temperature Sensor #%i %s - %s\u00B0C"
                % (
                    hardwaretypes[sensor.Hardware.HardwareType],
                    sensor.Hardware.Name,
                    sensor.Index,
                    sensor.Name,
                    sensor.Value,
                )
            )


import time

if __name__ == "__main__":
    while True:
        print("LibreHardwareMonitor:")
        HardwareHandle = initialize_librehardwaremonitor()
        fetch_stats(HardwareHandle)
        time.sleep(2)
    # print("\nCPUMonitor:")
    # CPUHandle = initialize_cputhermometer()
    # fetch_stats(CPUHandle)
