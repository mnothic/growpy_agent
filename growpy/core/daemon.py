__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "20140824"
__version__ = "1.0"
__author__ = "theManda"

import sys
import os
from growpy.core.collector import Collector
from growpy.core.config import config
from apscheduler.schedulers.blocking import BlockingScheduler


class Daemon:
    """
        A generic daemon class.
        Usage: subclass the daemon class and override the run() method.
    """
    def __init__(self, pid_file):
        self.pid_file = pid_file

    def detach(self):
        """Daemon class. UNIX double fork mechanism."""
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        # decouple from parent environment
        try:
            os.chdir('/')
            os.setsid()
            os.umask(0)
        except OSError:
            print("error os")

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as err:
                sys.stderr.write('fork #2 failed: {0}\n'.format(err))
                sys.exit(1)
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        pid = str(os.getpid())
        try:
            with open(self.pid_file, 'w+') as f:
                f.write(pid + '\n')
        except FileNotFoundError:
            print("pidfile {} Can not be crated or permissions denied.".format(self.pid_file))
            sys.exit(1)

    def start(self):
        """Start the daemon."""

        # Check for a pid_file to see if the daemon already runs
        try:
            with open(self.pid_file, 'r') as pf:
                pid = int(pf.read().strip())
        except FileNotFoundError:
            print("Can't read pidfile {}".format(self.pid_file))
            pid = None
        except ValueError:
            pid = None
        except IOError:
            pid = None

        if pid:
            message = "pid_file {0} already exist. " + \
                      "Daemon already running?\n"
            sys.stderr.write(message.format(self.pid_file))
            sys.exit(1)
        # Start the daemon
        self.detach()
        self.run()

    def run(self):
        print("Run as deamon...")
        agent = Collector()
        scheduler = BlockingScheduler(timezone='utc')
        scheduler.add_job(
            agent.main,
            'cron',
            month=config['scheduler']['month'],
            day=config['scheduler']['day'],
            hour=config['scheduler']['hour'],
            minute='*/10'
        )
        scheduler.start()