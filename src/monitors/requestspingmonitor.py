import requests

from src.base.basemonitor import BaseMonitor
from src.base.outagelevelobserver import OutageLevel


class RequestsPingMonitor(BaseMonitor):
    def __init__(self, endpoint: str, timeout: int, target_response_time: int):
        BaseMonitor.__init__(self)
        self.endpoint = endpoint
        self.timeout = timeout
        self.target = target_response_time

    def poll(self):
        try:
            time = requests.get(self.endpoint, timeout=self.timeout).elapsed.total_seconds() * 1000
            self.notify_quantitative(int(time), self.endpoint)
            self.notify_qualitative(True, self.endpoint)
            if time < self.target:
                self.debounce_outage(OutageLevel.UP, self.endpoint)
            else:
                self.debounce_outage(OutageLevel.DEGRADED_PERFORMANCE, self.endpoint)
        except:
            self.notify_quantitative(self.timeout, self.endpoint)
            self.debounce_outage(OutageLevel.DOWN, self.endpoint)
            self.notify_qualitative(False, self.endpoint)

