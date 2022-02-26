import json

import requests

from base.outagelevelobserver import OutageLevelObserver, OutageLevel
from base.quantitativeobserver import QuantitativeObserver

from secrets import *


class DiscordWebhook(OutageLevelObserver, QuantitativeObserver):
    def __init__(self):
        self.last_outage = OutageLevel.UP

    def notify_outage(self, value: OutageLevel, url: str):
        if value != self.last_outage:
            self.last_outage = value
            payload = {
                "content": None,
                "embeds": [
                    {
                        "title": "Estado del servidor",
                        "color": self.__get_color(self.last_outage),
                        "fields": [
                            {
                                "name": "URL",
                                "value": url,
                                "inline": True
                            },
                            {
                                "name": "Estado",
                                "value": self.__get_status(self.last_outage),
                                "inline": True
                            }
                        ]
                    }
                ]
            }
            for webhook in STATUS_WEBHOOKS:
                print("POST {}\n".format(webhook, json.dumps(payload)))
                if not DRY_MODE:
                    requests.post(webhook, data=json.dumps(payload),
                                  headers={"Content-Type": "application/json;charset=UTF-8"})

    def __get_color(self, outage: OutageLevel) -> int:
        hx = "00ff00"
        if outage == OutageLevel.PARTIAL_OUTAGE:
            hx = "ff8000"
        elif outage == OutageLevel.DEGRADED_PERFORMANCE:
            hx = "ffff00"
        elif outage == OutageLevel.DOWN:
            hx = "ff0000"
        return int(hx, 16)

    def __get_status(self, outage: OutageLevel) -> str:
        status = "OK"
        if outage == OutageLevel.PARTIAL_OUTAGE:
            status = "Caída parcial"
        elif outage == OutageLevel.DEGRADED_PERFORMANCE:
            status = "Rendimiento degradado"
        elif outage == OutageLevel.DOWN:
            status = "Caído"
        return status

    def notify_quantitative(self, value: int, url: str):
        payload = {
          "content": None,
          "embeds": [
            {
              "title": "Estado del servidor",
              "color": self.__get_color(self.last_outage),
              "fields": [
                {
                  "name": "URL",
                  "value": url,
                  "inline": True
                },
                {
                  "name": "Estado",
                  "value": self.__get_status(self.last_outage),
                  "inline": True
                },
                {
                  "name": "Latencia",
                  "value": str(value) + " ms",
                  "inline": True
                }
              ]
            }
          ]
        }
        for webhook in PING_WEBHOOKS:
            print("POST {}\n".format(webhook, json.dumps(payload)))
            if not DRY_MODE:
                requests.post(webhook, data=json.dumps(payload), headers={"Content-Type": "application/json;charset=UTF-8"})
