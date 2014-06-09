#!/usr/bin/env python

from distutils.core import setup

setup(name='Growpy',
      version='0.0.7',
      description='FileSystem statistic collector',
      author='Jorge A. Medina',
      author_email='jorge@bsdchile.cl',
      url='http://github.com/mnothic/growpy-agent',
      packages=['growpy/core', 'growpy/persistence'],
      data_files=[('/usr/local/etc/growpy/', 'core/config.py')],
      install_requires=['pycrypto>=2.6',
                        'paramiko>=1.7',
                        'SQLAlchemy>=0.8',
                        'APScheduler>=2.1'],
      license='BSD')

