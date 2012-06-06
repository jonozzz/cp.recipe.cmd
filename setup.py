# -*- coding: utf-8 -*-
# Copyright (C)2007 'Ingencpeb'

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
This module contains the tool of cp.recipe.cmd
"""
import os
from setuptools import setup, find_packages

version = '0.5dev'

name = 'cp.recipe.cmd'

setup(name=name,
      version=version,
      description="ZC Buildout recipe to execute commands in it's own shell",
      long_description=open("README.txt").read() + "\n" +
                       open("HISTORY.txt").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Buildout",
        ],
      keywords='buildout, zc.buildout, recipe',
      author='YUHSD #70',
      author_email='csawyer@yumaed.org',
      url='https://bitbucket.org/csawyer/cp.recipe.cmd/overview',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['cp.recipe','cp'],
      include_package_data=True,
      zip_safe=False,
      test_suite = "cp.recipe.cmd.tests.test_cmddocs.test_suite",
      install_requires=[
          'setuptools',
          'zc.buildout',
      ],
      entry_points = {"zc.buildout": [
                            "default = %s:Cmd" % name,
                            "sh = %s:Cmd" % name,
                            "py = %s:Python" % name,
                          ]
                       }
      )
