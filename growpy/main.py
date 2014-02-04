#!/usr/bin/env python
__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"

import sys
from time import sleep
from getopt import getopt, GetoptError
from growpy.core.collector import Collector
from growpy.core.config import config
from apscheduler.scheduler import Scheduler


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
        scheduler = Scheduler(standalone=False, daemonic=True)
        scheduler.add_cron_job(agent.main,
                               month=config['scheduler']['month'],
                               day=config['scheduler']['day'],
                               hour=config['scheduler']['hour'],)
        scheduler.start()
    elif process:
        print("Initializing growpy without scheduler")
        while True:
            agent.main()
            sleep(1)
    else:
        print("Initializing Scheduler standalone")
        scheduler = Scheduler(standalone=True)
        scheduler.add_cron_job(agent.main, minute='*', day='*', hour='17')
        scheduler.print_jobs()
        scheduler.start()