#!/usr/bin/env python

from setuptools import setup, find_packages


print(find_packages(exclude=["experiment", "tests", "techDocs"]))

setup(
    name='BluenetLib',
    version='0.0.1',
    packages=find_packages(exclude=["experiment", "tests", "techDocs"]),
 )