# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='shaolin',
    version='0.1b',
    description='Framework for interactive dashboards framework for the jupyter notebook',
    long_description=readme,
    author='Guillem Duran Ballester(HCSoft)',
    author_email='oficina@hcsoft.net',
    url='https://github.com/HCsoft-RD/shaolin',
    download_url = 'https://github.com/HCsoft-RD/shaolin/tarball/0.1b',
    keywords = ['dashboards', 'data vis', 'data analysis', 'shaolin'],
    packages=find_packages(exclude=['docs', 'examples', 'tests'])
)

