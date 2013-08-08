__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"

import sys
import os

from growpy.core.collector import Collector
from growpy.core.config import Config

prefix = os.getcwd()
BASE_DIRS = dict()
BASE_DIRS['install'] = prefix
BASE_DIRS['db'] = prefix + '/var/db/growpy'
BASE_DIRS['pidfile'] = prefix + '/var/run'
BASE_DIRS['etc'] = prefix + '/etc/growpy'


for key, value in BASE_DIRS.iteritems():
    if not os.path.exists(value):
        os.makedirs(value)

CFG = Config(BASE_DIRS['etc'] + '/growpy.cfg')

if __name__ == '__main__':
    agent = Collector(BASE_DIRS['pidfile'] + '/growpy.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            agent.start()
        elif 'stop' == sys.argv[1]:
            agent.stop()
        elif 'restart' == sys.argv[1]:
            agent.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print('usage: {} start|stop|restart'.format(sys.argv[0]))
        sys.exit(2)
