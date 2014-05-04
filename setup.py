#!/usr/bin/python
from setuptools import setup

setup(
  name='twitter_rec',
  version='0.01',
  maintainer='Justin and Eason',
  url='http://github.com/allenbo/twitter-rec',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Other Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 2.7',
  ],
  description='twitter-rec for big data course',
  package_dir={'': '.'},
  packages=['twitter_rec',] 
)
