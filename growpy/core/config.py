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
        cfg.read('/usr/local/etc/growpy.conf')
        cfg.read('/etc/growpy.conf')
    except parser.Error as e:
        print(e.message())

    config = {
        'core': {
            'pidfile': 'growpy.pid'
        },
        'database': {
            'provider': 'sqlite',
            'dbstring': growpy_data + '/growpy.db'
        },
        'scheduler': {
            'daemon': False,
            'month': '*',
            'day': '1',
            'hour': '0'
        }
    }

    def __init__(self):
        for section, value in self.config.items():
            for option in value.keys():
                try:
                    cfg_val = self.cfg.get(str(section), str(option))
                except(self.parser.NoSectionError, self.parser.NoOptionError) as e:
                    print(e.message)
                    continue
                self.config[section][option] = cfg_val

    def get_config(self):
        return self.config

cfg = Config()
config = cfg.get_config()