#!/usr/bin/env python

from distutils.core import setup

setup(name='Growpy',
      version='1.0',
      description='FileSystem stat information collector',
      author='Jorge A. Medina',
      author_email='j_at_engine_dot_cl',
      url='http://github.com/mnothic/growpy-agent',
      packages=['growpy/core', 'growpy/persistence'],
      data_files=[('/usr/local/etc/growpy/', 'core/config.py')],
      install_requires=['pycrypto>=2.6',
                        'paramiko>=1.14',
                        'SQLAlchemy>=0.9',
                        'APScheduler>=3.0'],
      license='BSD')

