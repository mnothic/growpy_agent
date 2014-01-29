__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"
import os
from growpy.core.base import Singleton


class Config(Singleton):
    growpy_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    growpy_etc = growpy_path + '/etc'
    growpy_data = growpy_path + '/data'
    growpy_scripts = growpy_path + '/scripts'
    try:
        import configparser
    except ImportError:
        import ConfigParser as configparser

    parser = configparser
    try:
        cfg = parser.ConfigParser()
        cfg.read(growpy_etc + '/growpy.conf')
    except parser.Error as e:
        print(e.message())

    config = {
        'core': {
            'pidfile': 'growpy.pid'
        },
        'database': {
            'dbstring': growpy_data + '/growpy.db',
            'provider': 'sqlite',
            'user': '',
            'password': '',
            'host': ''
        },
        'scheduler': {
            'daemon': False,
            'month': '*',
            'day': '1',
            'hour': '0'
        }
    }

    def __init__(self):
        for key, value in self.config.items():
            for val in value.items():
                try:
                    cfg_val = self.cfg.get(key, val)
                except(self.parser.NoSectionError, self.parser.NoOptionError) as e:
                    print(e.message)
                    continue
                self.config[key][val] = cfg_val

    def get_config(self):
        return self.config