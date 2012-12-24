#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

from setuptools import setup
from pywincmdtheme.info import NAME_SHORT, DESCR, VER_TXT

setup(
  name         = NAME_SHORT,
  version      = VER_TXT,
  description  = DESCR,
  author       = "Grigory Petrov",
  author_email = "grigory.v.p@gmail.com",
  url          = "http://bitbucket.org/eyeofhell/{0}".format( NAME_SHORT ),
  license      = 'GPLv3',
  packages     = [ NAME_SHORT ],
  zip_safe     = True,
  install_requires = [
    ##  Shortcuts to access windows API.
    'pywin32',
  ],
  entry_points = {
    'console_scripts' : [
      '{0} = {0}:main'.format( NAME_SHORT ),
    ],
  },
  ##  http://pypi.python.org/pypi?:action=list_classifiers
  classifiers  = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 2.7',
    'Topic :: Desktop Environment',
  ]
)

