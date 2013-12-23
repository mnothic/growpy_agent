__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"

import sys
import os
from getopt import getopt, GetoptError
from time import sleep

from growpy.core.collector import Collector
from growpy.core.config import Config

prefix = os.getcwd()
BASE_DIRS = dict()
BASE_DIRS['install'] = prefix
BASE_DIRS['db'] = prefix + '/var/db/growpy'
BASE_DIRS['pidfile'] = prefix + '/var/run'
BASE_DIRS['etc'] = prefix + '/etc/growpy'

demonize = False
for key, value in BASE_DIRS.iteritems():
    if not os.path.exists(value):
        os.makedirs(value)

CFG = Config(BASE_DIRS['etc'] + '/growpy.cfg')

if __name__ == '__main__':
    agent = Collector(BASE_DIRS['pidfile'] + '/growpy.pid')
    try:
        opts, args = getopt(sys.argv[1:], "c:d")
    except GetoptError as err:
        # print help information and exit:
        print(str(err))
    for o, a in opts:
        if o == 'd':
            demonize = True
        if o == 'c':
            cmd = a
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