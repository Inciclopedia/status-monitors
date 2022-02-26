from typing import Dict

from base.basemonitor import BaseMonitor
from monitors.requestspingmonitor import RequestsPingMonitor
from notifiers.discord_webhook import DiscordWebhook
from notifiers.statuspage import StatusPageNotifier
from secrets import *


def register() -> Dict[str, BaseMonitor]:
    monitors: Dict[str, BaseMonitor] = { url: RequestsPingMonitor(url, TIMEOUT_PING, DEGRADED_PERFORMANCE_TARGET_PING) for url in URLS }
    statuspage_observer = StatusPageNotifier()
    webhook_observer = DiscordWebhook()
    for monitor in monitors.values():
        monitor.register_outagelevel(statuspage_observer)
        monitor.register_outagelevel(webhook_observer)
        monitor.register_quantitative(statuspage_observer)
        monitor.register_quantitative(webhook_observer)
    return monitors
