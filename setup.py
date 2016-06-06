# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='shaolin',
    version='0.1',
    description='Framework for interactive data visualization in the jupyter notebook',
    long_description=readme,
    author='Guillem Duran Ballester(HCSoft)',
    author_email='oficina@hcsoft.net',
    url='https://github.com/HCsoft-RD/shaolin',
    download_url = 'https://github.com/HCsoft-RD/shaolin/tarball/0.1',
    keywords = ['dashboards', 'data vis', 'data analysis', 'shaolin']
    license=license,
    packages=['shaolin']
)

