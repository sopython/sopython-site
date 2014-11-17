#!/usr/bin/env python
import os
import re
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'sopy', '__init__.py')) as f:
    version = re.search(r"__version__ = '(.*)'", f.read()).group(1)

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='sopy',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    url='http://sopython.com/',
    license='BSD',
    author='David Lord',
    author_email='davidism@gmail.com',
    description='The productive programming cabbage website.',
    entry_points={'console_scripts': ['sopy = sopy.manage:cli.main']},
    install_requires=requirements
)
