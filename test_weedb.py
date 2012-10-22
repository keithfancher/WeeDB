#!/usr/bin/env python


# Copyright 2012 Keith Fancher
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


import StringIO
import sys
import unittest
import weedb


class TestCommands(unittest.TestCase):

    def setUp(self):
        """Create a test instance and redirect stdout for testing."""
        self.db = weedb.WeeDB()
        self.output = StringIO.StringIO()
        self.saved_stdout = sys.stdout
        sys.stdout = self.output

    def tearDown(self):
        """Fix stdout now that we're through."""
        self.output.close()
        sys.stdout = self.saved_stdout

    def test_set(self):
        self.db._set('a', '10')
        self.assertEqual(self.db._db['a'], '10')

    def test_get(self):
        self.db._db['a'] = '10'
        self.db._get('a')
        self.assertEqual(self.output.getvalue(), "10\n")

    def test_unset(self):
        self.db._db['bleep'] = 'bloop'
        self.db._unset('bleep')
        self.assertEqual(self.db._db.get('bleep'), None)

    def test_numequalto(self):
        self.db._db = {'a': '10', 'b': '10', 'c': '20', 'd': '10'}
        self.db._numequalto('10')
        self.assertEqual(self.output.getvalue(), "3\n")


if __name__ == '__main__':
    unittest.main()
