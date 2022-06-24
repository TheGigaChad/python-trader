#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import setuptools

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setuptools.setup(name='pytrader',
                 version='0.0.3',
                 author='Michael Judd',
                 author_email='MichaelJuddNZ@gmail.com',
                 description='Python Trader',
                 url='https://github.com/TheGigaChad/python-trader',
                 packages=['pytrader', 'pytrader.common', 'pytrader.models', 'pytrader.ml'],
                 scripts=['bin/ptTrain'],
                 install_requires=install_requires)
