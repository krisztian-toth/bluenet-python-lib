#!/usr/bin/env python3

from setuptools import setup, find_packages


print(find_packages(exclude=["examplesUsb", "experiment", "tests", "techDocs"]))

setup(
    name='BluenetLib',
    version='0.5.4',
    packages=find_packages(exclude=["examples", "experiment", "tests", "techDocs"]),
    install_requires=[
        'pyserial==3.4.0',
        'bluepy==1.1.4',
        'pyaes==1.6.1',
        'requests==2.18.4'
    ],
    dependency_links=[
        'http://github.com/crownstone/bluepy/tarball/master#egg=bluepy-1.1.4',
        'http://github.com/requests/requests/tarball/a3d7cf3f27e74c28ef30f01e9f2e483570ab042e#egg=requests-2.18.4'
    ]
)
