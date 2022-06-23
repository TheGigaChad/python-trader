#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import setuptools

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setuptools.setup(name='pytrader',
                 version='0.0.1',
                 author='Michael Judd',
                 author_email='MichaelJuddNZ@gmail.com',
                 description='Python Trader',
                 url='https://github.com/TheGigaChad/python-trader',
                 packages=setuptools.find_packages(),
                 install_requires=install_requires)
