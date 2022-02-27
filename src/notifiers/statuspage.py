import json
import time

from base.outagelevelobserver import OutageLevelObserver, OutageLevel
from base.quantitativeobserver import QuantitativeObserver
import requests

from secrets import *

INCIDENT_MARGIN = 21600


class StatusPageNotifier(OutageLevelObserver, QuantitativeObserver):
    def __init__(self):
        self.last_incident_time = None

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

    def notify_incident(self, url):
        if url not in STATUSPAGE_COMPONENTS.keys():
            return
        component = STATUSPAGE_COMPONENTS[url]
        body = {
          "incident": {
            "name": "Problemas de conectividad con el wiki",
            "status": "investigating",
            "impact_override": "none",
            "deliver_notifications": True,
            "auto_transition_deliver_notifications_at_end": True,
            "auto_transition_deliver_notifications_at_start": True,
            "auto_transition_to_maintenance_state": True,
            "auto_transition_to_operational_state": True,
            "auto_tweet_at_beginning": True,
            "auto_tweet_on_completion": True,
            "auto_tweet_on_creation": True,
            "auto_tweet_one_hour_before": True,
            "body": "Nuestros sistemas han detectado problemas de conectividad con el wiki. Nuestros técnicos han sido notificados y una investigación del problema comenzará a la mayor brevedad.",
            "components": {
              component: OutageLevel.DOWN
            },
            "component_ids": [
              component
            ]
          }
        }

        print("POST https://api.statuspage.io/v1/pages/{}/incidents".format(STATUSPAGE_PAGE_ID))
        print(json.dumps(body))
        if not DRY_MODE:
            requests.post("https://api.statuspage.io/v1/pages/{}/incidents".format(STATUSPAGE_PAGE_ID),
                           headers={"Authorization": "Oauth {}".format(STATUSPAGE_API_KEY)},
                           json=body)

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
        if value == OutageLevel.DOWN and self.last_incident_time is None or time.time() - self.last_incident_time > INCIDENT_MARGIN:
            self.last_incident_time = time.time()
            self.notify_incident(url)

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
