from typing import Final, Dict
from pathlib import Path

COMMON_DIR_PATH: Path = Path(__file__).parent

DLLS_FILE_LOCATION_DICT: Final[Dict[str, str]] = {
    "libremonitor_dll": COMMON_DIR_PATH.joinpath(
        "dlls/LibreHardwareMonitorLib.dll"
    ).as_posix(),
    "hidsharp_dll": COMMON_DIR_PATH.joinpath(
        "dlls/HidSharp.dll"
    ).as_posix(),  # if this is not added libre hardware fails,
}


class GlobalConstants:
    LIBREMONITOR_DLL_NAMESPACE: Final[str] = "LibreHardwareMonitor"
