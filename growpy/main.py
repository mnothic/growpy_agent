#!/usr/bin/env python
__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "20140824"
__version__ = "1.0"
__author__ = "theManda"

import sys
from time import sleep
from getopt import getopt, GetoptError
from growpy.core.collector import Collector
from growpy.core.config import config
from apscheduler.schedulers.blocking import BlockingScheduler
daemon = False
process = False

if __name__ == '__main__':
    agent = Collector()
    try:
        opts, args = getopt(sys.argv[1:], "dp")
    except GetoptError as err:
        # print help information and exit:
        print(str(err))
    for flag, value in opts:
        if flag == '-d':
            daemon = True
        if flag == '-p':
            process = True
    if daemon:
        scheduler = BlockingScheduler(timezone='utc')
        scheduler.add_job(
            agent.main,
            'cron',
            month=config['scheduler']['month'],
            day=config['scheduler']['day'],
            hour=config['scheduler']['hour']
        )
        scheduler.start()
        print("Exit main thread")
    elif process:
        print("Initializing growpy without scheduler")
        import time
        while True:
            start = time.time()
            agent.main()
            print("Threads Time Elapsed: {}", time.time() - start)
            sleep(60)
    else:
        print("Initializing Scheduler standalone")
        scheduler = BlockingScheduler(timezone='utc')
        scheduler.add_job(agent.main, 'cron', hour='*', minute='*/5')
        scheduler.start()
        print("Exit main thread")