#!/usr/bin/env python
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='sopy',
    version='1.2.2-dev',
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
