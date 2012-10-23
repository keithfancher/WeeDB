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
        self.assertEqual(self.db._transactions[0]['a'], '10')

    def test_get(self):
        self.db._transactions[0]['a'] = '10'
        self.db._get('a')
        self.assertEqual(self.output.getvalue(), "10\n")
        self.db._get('asdf')
        self.assertEqual(self.output.getvalue(), "10\nNULL\n")

    def test_unset(self):
        self.db._transactions[0]['bleep'] = 'bloop'
        self.db._unset('bleep')
        self.assertEqual(self.db._transactions[0].get('bleep'), None)

    def test_numequalto(self):
        self.db._transactions[0]['a'] = '10'
        self.db._transactions[0]['b'] = '10'
        self.db._transactions[0]['c'] = '20'
        self.db._transactions[0]['d'] = '10'
        self.db._numequalto('10')
        self.assertEqual(self.output.getvalue(), "3\n")

    def test_commit_deletes_null_values(self):
        """After committing all open transactions, values that were "unset" in
        a transactional layer should be fully removed from the database."""
        self.db._set('a', '10')
        self.db._begin()
        self.db._unset('a')
        self.db._commit()
        with self.assertRaises(KeyError):
            self.db._transactions[0]['a']


class TestThumbtackGivenInput(unittest.TestCase):

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

    def test_sample_input_01(self):
        self.db._set('a', '10')
        self.db._get('a')
        self.db._unset('a')
        self.db._get('a')
        self.assertEqual(self.output.getvalue(), "10\nNULL\n")

    def test_sample_input_02(self):
        self.db._set('a', '10')
        self.db._set('b', '10')
        self.db._numequalto('10')
        self.db._numequalto('20')
        self.db._unset('a')
        self.db._numequalto('10')
        self.db._set('b', '30')
        self.db._numequalto('10')
        self.assertEqual(self.output.getvalue(), "2\n0\n1\n0\n")

    def test_sample_input_03(self):
        self.db._begin()
        self.db._set('a', '10')
        self.db._get('a')
        self.db._begin()
        self.db._set('a', '20')
        self.db._get('a')
        self.db._rollback()
        self.db._get('a')
        self.db._rollback()
        self.db._get('a')
        self.assertEqual(self.output.getvalue(), "10\n20\n10\nNULL\n")

    def test_sample_input_04(self):
        self.db._begin()
        self.db._set('a', '30')
        self.db._begin()
        self.db._set('a', '40')
        self.db._commit()
        self.db._get('a')
        self.db._rollback()
        self.assertEqual(self.output.getvalue(), "40\nINVALID ROLLBACK\n")

    def test_sample_input_05(self):
        self.db._set('a', '50')
        self.db._begin()
        self.db._get('a')
        self.db._set('a', '60')
        self.db._begin()
        self.db._unset('a')
        self.db._get('a')
        self.db._rollback()
        self.db._get('a')
        self.db._commit()
        self.db._get('a')
        self.assertEqual(self.output.getvalue(), "50\nNULL\n60\n60\n")

    def test_sample_input_06(self):
        self.db._set('a', '10')
        self.db._begin()
        self.db._numequalto('10')
        self.db._begin()
        self.db._unset('a')
        self.db._numequalto('10')
        self.db._rollback()
        self.db._numequalto('10')
        self.assertEqual(self.output.getvalue(), "1\n0\n1\n")


if __name__ == '__main__':
    unittest.main()
