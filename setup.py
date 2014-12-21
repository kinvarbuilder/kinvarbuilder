#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'kinvarbuilder',
    version = '0.0',
    url = 'https://github.com/kinvarbuilder/kinvarbuilder/',
    license = 'Apache Software License Version 2.0',
    author = 'Andre Holzner',
    tests_require = [],
    install_requires = [],
    author_email = 'andre.holzner@gmail.com',
    description = 'A library for building kinematic variables systematically',
    long_description = '',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    classifiers = [
        'Programming Language :: Python',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        ],
    extras_require = { }
)

