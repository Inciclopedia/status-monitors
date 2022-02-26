from abc import ABC, abstractmethod


class QuantitativeObserver(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def notify_quantitative(self, value: int, url: str):
        raise NotImplementedError
