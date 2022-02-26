from registrations.modules import register
from secrets import *
import sched
import time

monitors = register()


def poll(sch):
    global monitors
    for monitor in monitors.values():
        monitor.poll()
    sch.enter(POLL_TIME, 1, poll, (sch,))


scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enter(POLL_TIME, 1, poll, (scheduler,))
scheduler.run()



