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


class TestCommands(unittest.TestCase):

    def setUp(self):
        self.db = weedb.WeeDB()

    def test_set(self):
        self.db._set('a', '10')
        self.assertEqual(self.db._db['a'], '10')

    def test_get(self):
        pass

    def test_unset(self):
        self.db._db['bleep'] = 'bloop'
        self.db._unset('bleep')
        self.assertEqual(self.db._db.get('bleep'), None)


if __name__ == '__main__':
    unittest.main()
