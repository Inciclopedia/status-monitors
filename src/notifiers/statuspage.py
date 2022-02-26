import json
import time

from base.outagelevelobserver import OutageLevelObserver, OutageLevel
from base.quantitativeobserver import QuantitativeObserver
import requests

from secrets import *


class StatusPageNotifier(OutageLevelObserver, QuantitativeObserver):
    def __init__(self):
        pass

    def __convert_outage(self, value: OutageLevel) -> str:
        if value == OutageLevel.UP:
            return "operational"
        elif value == OutageLevel.DOWN:
            return "major_outage"
        elif value == OutageLevel.DEGRADED_PERFORMANCE:
            return "degraded_performance"
        elif value == OutageLevel.PARTIAL_OUTAGE:
            return "partial_outage"
        return "operational"

    def notify_outage(self, value: OutageLevel, url: str):
        if url not in STATUSPAGE_COMPONENTS.keys():
            return
        component = STATUSPAGE_COMPONENTS[url]
        body = {"component": {
                           "status": self.__convert_outage(value)
                       }}
        print("PATCH https://api.statuspage.io/v1/pages/{}/components/{}".format(STATUSPAGE_PAGE_ID, component))
        print(json.dumps(body))
        if not DRY_MODE:
            requests.patch("https://api.statuspage.io/v1/pages/{}/components/{}".format(STATUSPAGE_PAGE_ID, component),
                           headers={"Authorization": "Oauth {}".format(STATUSPAGE_API_KEY)},
                           json=body)

    def notify_quantitative(self, value: int, url: str):
        if url not in STATUSPAGE_METRICS.keys():
            return
        metric = STATUSPAGE_METRICS[url]
        body = {"data": {
                          metric: [
                              {
                                  "timestamp": int(time.time()),
                                  "value": value
                              }
                          ]
                      }
            }
        print("POST https://api.statuspage.io/v1/pages/{}/metrics/data".format(STATUSPAGE_PAGE_ID))
        print(json.dumps(body))
        if not DRY_MODE:
            requests.post("https://api.statuspage.io/v1/pages/{}/metrics/data".format(STATUSPAGE_PAGE_ID),
                          headers={"Authorization": "Oauth {}".format(STATUSPAGE_API_KEY)},
                          json=body)
