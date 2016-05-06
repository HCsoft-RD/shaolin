# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='shaolin',
    version='0.0.1',
    description='Interactive data visualization for the jupyter notebook',
    long_description=readme,
    author='Guillem Duran Ballester(HCSoft)',
    author_email='oficina@hcsoft.net',
    url='https://github.com/HCsoft-RD/shaolin',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

