#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='chronoplot',
    version='0.1.0',
    description='Timeline maker.',
    long_description='',
    keywords='',
    url='https://github.com/darkfeline/chronoplot',
    author='Allen Li',
    author_email='darkfeline@felesatra.moe',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3.5',
    ],

    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'chronoplot = chronoplot.main:main',
        ],
    },
)
