__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"

config = {
    'core': {
        'schedule_time': 'montly',
        'pidfile': 'growpy.pid'
    },
    'database': {
        'dbstring': '/home/themanda/PycharmProjects/webfront/delta.db',
        'provider': 'sqlite'
    },
    'scheduler': {
        'daemon': False,
        'month': '*',
        'day': '1',
        'hour': '0'
    }
}
