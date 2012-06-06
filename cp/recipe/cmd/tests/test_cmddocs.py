# -*- coding: utf-8 -*-
# Copyright (C)2007 'Ingeniweb'

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
Generic Test case for 'cp.recipe.cmd' doctest
"""
__docformat__ = 'restructuredtext'

import zc.buildout.tests
import zc.buildout.testing

import unittest
import doctest
import sys
import os
from os.path import join

from zope.testing import doctest, renormalizing

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('iw.recipe.template', test)

tearDown=zc.buildout.testing.buildoutTearDown

current_dir = os.path.dirname(__file__)

def doc_suite(test_dir, setUp=setUp, tearDown=tearDown, globs=None):
    """Returns a test suite, based on doctests found in /doctest."""
    suite = []
    if globs is None:
        globs = globals()

    globs['test_dir'] = current_dir

    flags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE |
             doctest.REPORT_ONLY_FIRST_FAILURE)

    package_dir = os.path.split(test_dir)[0]
    if package_dir not in sys.path:
        sys.path.append(package_dir)

    doctest_dir = os.path.join(package_dir, 'docs')

    # filtering files on extension
    docs = [os.path.join(doctest_dir, doc) for doc in
            os.listdir(doctest_dir) if doc.endswith('.txt')]

    globs['test_dir'] = current_dir

    for test in docs:
        suite.append(doctest.DocFileSuite(test, optionflags=flags,
                                          globs=globs, setUp=setUp,
                                          tearDown=tearDown,
                                          module_relative=False,
                                          checker=renormalizing.RENormalizing([
                                                    zc.buildout.testing.normalize_path,
                                            ])))

    return unittest.TestSuite(suite)

def test_suite():
    """returns the test suite"""
    return doc_suite(current_dir)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

