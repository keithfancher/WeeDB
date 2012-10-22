#!/usr/bin/env python


# Copyright 2012 Keith Fancher
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


import unittest
import weedb


class TestWeeDB(unittest.TestCase):

    def setUp(self):
        self.db = weedb.WeeDB()

    def test_parse_command(self):
        pass

    def test_is_valid_command_good(self):
        """Valid commands should return True."""
        valid_commands = ['SET', 'GET', 'UNSET', 'NumEqualTo', 'end',
                          'bEGIN', 'ROLLBACK', 'cOMmIt']
        invalid_commands = ['s3t', 'whatever', 'SETGETBLARG', 'some thing']
        for com in valid_commands:
            self.assertTrue(self.db._is_valid_command(com))

    def test_is_valid_command_bad(self):
        """Invalid commands should return False."""
        invalid_commands = ['s3t', 'whatever', 'SETGETBLARG', 'some thing']
        for com in invalid_commands:
            self.assertFalse(self.db._is_valid_command(com))


if __name__ == '__main__':
    unittest.main()
