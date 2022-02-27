from abc import ABC, abstractmethod
from typing import List, Dict

from secrets import OUTAGE_CHANGE_AFTER
from base.outagelevelobserver import OutageLevelObserver, OutageLevel
from base.qualitativeobserver import QualitativeObserver
from base.quantitativeobserver import QuantitativeObserver


class BaseMonitor(ABC):

    @abstractmethod
    def __init__(self):
        self.quantitative_observers: List[QuantitativeObserver] = []
        self.qualitative_observers: List[QualitativeObserver] = []
        self.outage_observers: List[OutageLevelObserver] = []
        self.outage_counters: Dict[str, int] = {}
        self.current_status: Dict[str, OutageLevel] = {}
        self.upcoming_status: Dict[str, OutageLevel] = {}

    def register_quantitative(self, observer: QuantitativeObserver):
        self.quantitative_observers.append(observer)

    def register_qualitative(self, observer: QualitativeObserver):
        self.qualitative_observers.append(observer)

    def register_outagelevel(self, observer: OutageLevelObserver):
        self.outage_observers.append(observer)

    def notify_quantitative(self, value: int, url: str):
        for observer in self.quantitative_observers:
            observer.notify_quantitative(value, url)

    def notify_qualitative(self, value: bool, url: str):
        for observer in self.qualitative_observers:
            observer.notify_qualitative(value, url)

    def notify_outage(self, value: OutageLevel, url: str):
        for observer in self.outage_observers:
            observer.notify_outage(value, url)

    def debounce_outage(self, value: OutageLevel, url: str):
        if url not in self.current_status:
            self.current_status[url] = value
            self.notify_outage(value, url)
        elif value != self.current_status[url]:
            if url not in self.upcoming_status or value != self.upcoming_status[url]:
                self.upcoming_status[url] = value
                self.outage_counters[url] = 0
            elif value == self.upcoming_status[url]:
                self.outage_counters[url] += 1
                if self.outage_counters[url] >= OUTAGE_CHANGE_AFTER:
                    self.current_status[url] = value
                    self.notify_outage(value, url)
                    del self.upcoming_status[url]
                    del self.outage_counters[url]
        elif value == self.current_status[url]:
            del self.upcoming_status[url]
            del self.outage_counters[url]

    @abstractmethod
    def poll(self):
        raise NotImplementedError
