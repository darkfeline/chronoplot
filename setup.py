#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='chronos',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'chronos = chronos.main:main',
        ],
    },

    author='Allen Li',
    author_email='darkfeline@felesatra.moe',
    description='Timeline maker.',
    license='GPLv3',
    url='',
)