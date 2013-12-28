#!/usr/bin/env python
"""
the install_requieres only works with setuptools and I need more knowledge
because not always be installed on systems de built-in package is distutils.
"""
from distutils.core import setup

setup(name='Growpy',
      version='0.0.7',
      description='FileSystem statistic collector',
      author='Jorge A. Medina',
      author_email='jorge@bsdchile.cl',
      url='http://github.com/mnothic/growpy-agent',
      packages=['growpy'],
      install_requires=['paramiko>=1.7',
                        'SQLAlchemy>=0.8',
                        'APScheduler>=2.1'],
      license='BSD',
      )

