#!/usr/bin/env python2

import io
import os

from setuptools import find_packages, setup, command

NAME = 'src'
DESCRIPTION = 'Project for a lecture about Algorithm Engineering'

REQUIRED = [
    'requests', 'scapy', 'pygal',
]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=long_description,
    packages=find_packages(),
    install_requires=REQUIRED,
    include_package_data=True,
)
