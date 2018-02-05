#!/usr/bin/env python
from setuptools import setup, find_packages

with open('README.rst', encoding='utf8') as f:
    readme = f.read()

setup(
    name='sopy',
    version='1.8',
    url='http://sopython.com/',
    author='David Lord',
    author_email='davidism@gmail.com',
    license='BSD',
    description='The productive programming cabbage website.',
    long_description=readme,
    zip_safe=False,
    python_requires='>=3.4',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-Alembic',
        'Flask-Babel',
        'Flask-Mail',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'beautifulsoup4',
        'hoep',
        'inflection',
        'lxml',
        'psycopg2',
        'Pygments',
        'requests',
    ],
    extras_require={
        'dev': [
            'Flask-Shell-IPython',
            'Sphinx',
        ]
    },
    entry_points = {
        'console_scripts': [
            'sopy = sopy.cli:main',
        ],
    },
)
