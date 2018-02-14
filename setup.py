#!/usr/bin/env python

from setuptools import setup, find_packages


print(find_packages(exclude=["examples", "experiment", "tests", "techDocs"]))

setup(
    name='BluenetLib',
    version='0.0.2',
    packages=find_packages(exclude=["examples", "experiment", "tests", "techDocs"]),
    install_requires=[
        'pyserial==3.4.0',
    ],
 )