from abc import abstractmethod, ABCMeta


class ILibreMonitorAdapter(ABCMeta):
    @classmethod
    @abstractmethod
    def from_libremonitor_hardware(cls, libremonitor_hardware) -> object:
        pass
