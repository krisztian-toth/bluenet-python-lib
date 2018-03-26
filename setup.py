#!/usr/bin/env python

from setuptools import setup, find_packages


print(find_packages(exclude=["examples", "experiment", "tests", "techDocs"]))

setup(
    name='BluenetLib',
    version='0.1.0',
    packages=find_packages(exclude=["examples", "experiment", "tests", "techDocs"]),
    install_requires=[
        'pyserial==3.4.0',
        'pyaes==1.6.1',
        'requests==2.18.4'
    ],
    dependency_links=['http://github.com/requests/requests/tarball/a3d7cf3f27e74c28ef30f01e9f2e483570ab042e#egg=requests-2.18.4']
)