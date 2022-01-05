#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import setuptools

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setuptools.setup(name='pytrader',
                 packages=['pytrader'],
                 install_requires=install_requires)
