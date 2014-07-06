#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='sopy',
    version='0.0.0',
    packages=find_packages(),
    url='http://sopython.com/',
    license='BSD',
    author='Ffisegydd',
    author_email='ffisegydd@sopython.com',
    description='The productive programming cabbage website.',
    entry_points={
        'console_scripts': [
            'sopy = sopy.manage:cli.main',
        ],
    },
)
