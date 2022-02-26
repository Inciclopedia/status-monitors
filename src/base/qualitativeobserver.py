from abc import ABC, abstractmethod


class QualitativeObserver(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def notify_qualitative(self, value: bool, url: str):
        raise NotImplementedError
