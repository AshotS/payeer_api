#!/usr/bin/env python
from os.path import join, dirname
from setuptools import setup, find_packages

setup(name='payeer_api',
      version='0.1',
      description='Python Payeer API client',
      long_description=open(join(dirname(__file__), 'README.rst'),encoding='utf-8').read(),
      author='AshotS',
      author_email='sarckisyanashot@yandex.ru',
      url='https://github.com/AshotS/payeer_api',
      packages=['payeer_api'],
      requires=['requests'],
      license='MIT license',
      keywords="payeer",
      )
