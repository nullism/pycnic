#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))
from pycnic import __version__

setup(name='pycnic',
    version = __version__,
    description = 'A simple, ultra light-weight, pure-python RESTful JSON API framework.',
    long_description = (
        'Pycnic offers a fully WSGI compliant JSON only web framework for '
        'quickly creating fast, modern web applications '
        'based on AJAX. Static files are served over a CDN or ' 
        'with a standard webserver, like Apache.'),
    author = 'Aaron Meier',
    author_email = 'webgovernor@gmail.com',
    packages = ['pycnic'],
    package_dir={'pycnic':'pycnic'},
    url = 'http://pycnic.nullism.com',
    license = 'MIT',
    install_requires = [],
    provides = ['pycnic']
)

