#!/usr/bin/env python
__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "20140824"
__version__ = "1.0"
__author__ = "theManda"

import sys
from time import sleep, time
from getopt import getopt, GetoptError
from growpy.core.collector import Collector
from growpy.core.daemon import Daemon
from growpy.core.config import config
from apscheduler.schedulers.blocking import BlockingScheduler

daemon = False
process = False

""" Usage: growpy [option]
Options:
    -d
    -p
    -h | --help
    --version
"""


def main():
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
        detach = Daemon(config['core']['pidfile'])
        detach.start()
        print("Exit main thread")
    elif process:
        agent = Collector()
        print("Initializing growpy without scheduler")
        while True:
            start = time()
            agent.main()
            print("Threads Time Elapsed: {}", time() - start)
            sleep(60)
    else:
        agent = Collector()
        print("Initializing Scheduler standalone")
        scheduler = BlockingScheduler(timezone='utc')
        scheduler.add_job(agent.main, 'cron', hour='*', minute='*/5')
        scheduler.start()
        print("Exit main thread")


if __name__ == '__main__':
    main()