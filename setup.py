#!/usr/bin/env python

from setuptools import setup, find_packages


print(find_packages(exclude=["examples", "experiment", "tests", "techDocs"]))

setup(
    name='BluenetLib',
    version='0.0.2',
    packages=find_packages(exclude=["examples", "experiment", "tests", "techDocs"]),
    install_requires=[
        'pyserial==3.4.0',
        'bluepy==1.1.4',
        'pyaes==1.6.1'
    ],
    dependency_links=['http://github.com/crownstone/bluepy/tarball/master#egg=bluepy-1.1.4']
)