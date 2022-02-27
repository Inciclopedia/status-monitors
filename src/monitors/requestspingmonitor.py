import requests

from base.basemonitor import BaseMonitor
from base.outagelevelobserver import OutageLevel


class RequestsPingMonitor(BaseMonitor):
    def __init__(self, endpoint: str, timeout: int, target_response_time: int):
        BaseMonitor.__init__(self)
        self.endpoint = endpoint
        self.timeout = timeout
        self.target = target_response_time

    def poll(self):
        try:
            response = requests.get(self.endpoint, timeout=self.timeout)
            time = response.elapsed.total_seconds() * 1000
            if response.status_code >= 400:
                self.notify_quantitative(int(time), self.endpoint)
                self.notify_qualitative(False, self.endpoint)
                self.debounce_outage(OutageLevel.DOWN, self.endpoint)
                return
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

