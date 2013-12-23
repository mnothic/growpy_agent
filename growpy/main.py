__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"

import sys
import os
from getopt import getopt, GetoptError
from time import sleep
from growpy.core.collector import Collector
from growpy.core.config import config

demonize = False

if __name__ == '__main__':
    agent = Collector()
    try:
        opts, args = getopt(sys.argv[1:], "c:d")
    except GetoptError as err:
        # print help information and exit:
        print(str(err))
    for flag, value in opts:
        if flag == 'd':
            demonize = True
        if flag == 'c':
            cmd = value
    if demonize:
        if 'start' == cmd:
            agent.start()
        elif 'stop' == cmd:
            agent.stop()
        elif 'restart' == cmd:
            agent.restart()
        else:
            print('usage: {} -d -c start|stop|restart'.format(sys.argv[0]))
            sys.exit(2)
    else:
        while True:
            agent.main()
            sleep(3)