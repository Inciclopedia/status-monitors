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

    def __get_color(self, outage: OutageLevel) -> int:
        hx = "00ff00"
        if outage == OutageLevel.PARTIAL_OUTAGE:
            hx = "ff8000"
        elif outage == OutageLevel.DEGRADED_PERFORMANCE:
            hx = "ffff00"
        elif outage == OutageLevel.DOWN:
            hx = "ff0000"
        return int(hx, 16)

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
                  "value": "http://inciclopedia.org",
                  "inline": True
                },
                {
                  "name": "Estado",
                  "value": "OK",
                  "inline": True
                },
                {
                  "name": "Latencia",
                  "value": "200 ms",
                  "inline": True
                }
              ]
            }
          ]
        }
        for webhook in DISCORD_WEBHOOKS:
            if DRY_MODE:
                print("POST {}\n".format(webhook, json.dumps(payload)))
            else:
                requests.post(webhook, data=json.dumps(payload), headers={"Content-Type": "application/json;charset=UTF-8"})
