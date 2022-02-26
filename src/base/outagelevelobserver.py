from abc import ABC, abstractmethod
from enum import Enum


class OutageLevel(Enum):
    DOWN = 0
    UP = 1
    DEGRADED_PERFORMANCE = 2
    PARTIAL_OUTAGE = 3


class OutageLevelObserver(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def notify_outage(self, value: OutageLevel, url: str):
        raise NotImplementedError
