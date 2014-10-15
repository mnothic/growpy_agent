__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "1"
__version__ = "1.0"
__author__ = "theManda"
import os
from configparser import ConfigParser
from growpy.core.base import Singleton


class Config(metaclass=Singleton):
    growpy_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    growpy_etc = growpy_path + '/etc'
    growpy_data = growpy_path + '/data'
    growpy_scripts = growpy_path + '/scripts'
    try:
        cfg = ConfigParser()
        cfg.read(growpy_etc + '/growpy.conf')
        cfg.read('/usr/local/etc/growpy.conf')
        cfg.read('/etc/growpy.conf')
    except ConfigParser.Error as e:
        print(e.message())
        exit(1)

    config = {
        'core': {
            'pidfile': 'growpy.pid',
            'debug': True,
            'aes_key': 'growpy'
        },
        'database': {
            'db_url': 'sqlite:///growypy.db',
        },
        'scheduler': {
            'daemon': False,
            'month': '*',
            'day': '1',
            'hour': '0'
        }
    }

    def __init__(self):
        """refactory this bullshit with pythonic iterator"""
        for section, value in self.config.items():
            for option in value.keys():
                try:
                    cfg_val = self.cfg.get(str(section), str(option))
                except(self.parser.NoSectionError, self.parser.NoOptionError) as e:
                    print(e.message)
                    continue
                if option == 'debug':
                    if cfg_val == 'True':
                        cfg_val = True
                    elif cfg_val == 'False':
                        cfg_val = False
                    else:
                        print("Parse error debug flag must be True or False")
                self.config[section][option] = cfg_val

    def get_config(self):
        return self.config

cfg = Config()
config = cfg.get_config()