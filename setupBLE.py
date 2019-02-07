#!/usr/bin/env python3

from setuptools import setup, find_packages


print(find_packages(exclude=["examplesUsb", "experiment", "tests", "techDocs"]))

setup(
    name='BluenetLib',
    version='0.6.2',
    packages=find_packages(exclude=["examples", "experiment", "tests", "techDocs"]),
    install_requires=[
        'pyserial==3.4.0',
        'bluepy==1.1.4',
        'pyaes==1.6.1',
        'requests==2.20.1'
    ],
    dependency_links=[
        'http://github.com/crownstone/bluepy/tarball/master#egg=bluepy-1.1.4',
        'http://github.com/requests/requests/tarball/6cfbe1aedd56f8c2f9ff8b968efe65b22669795b#egg=requests-2.20.1'
    ]
)
