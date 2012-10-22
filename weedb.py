#!/usr/bin/env python


# Copyright 2012 Keith Fancher
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


import sys


class InvalidCommandError(Exception):
    pass


class InvalidArgumentError(Exception):
    pass


class WeeDB(object):

    def __init__(self):
        self._db = {}
        self._commands = { 'SET': self._set,
                           'GET': self._get,
                           'UNSET': self._unset,
                           'NUMEQUALTO': self._numequalto,
                           'END': self._end,
                           'BEGIN': self._begin,
                           'ROLLBACK': self._rollback,
                           'COMMIT': self._commit }

    def execute_command(self, input_command):
        """Parse and execute a database command, passed as a string. Can raise
        either an InvalidCommandError or InvalidArgumentError if the input is
        bad."""
        command, args = self._parse_command(input_command)
        try:
            self._commands[command](*args)
        except KeyError:
            raise InvalidCommandError("Sorry, WeeDB doesn't know that one.")
        except TypeError:
            raise InvalidArgumentError('Invalid argument(s)!')

    def _parse_command(self, command):
        """Parse a command string and return a tuple of (command, [args]),
        where args is a list of arguments."""
        com_list = command.split()
        return (com_list[0].upper(), com_list[1:])

    def _set(self, name, value):
        self._db[name] = value

    def _get(self, name):
        print self._db[name]

    def _unset(self, name):
        del self._db[name]

    def _numequalto(self, value):
        print 'numequalto ' + value

    def _end(self):
        sys.exit(0)

    def _begin(self):
        print 'begin'

    def _rollback(self):
        print 'rollback'

    def _commit(self):
        print 'commit'


def main():
    """My main() man."""
    db = WeeDB()

    print 'Welcome to WeeDB. Have a tiny bit of fun!'
    while True:
        command = raw_input('>>> ')
        try:
            db.execute_command(command)
        except InvalidCommandError:
            print "Sorry, I don't know that command!"
        except InvalidArgumentError:
            print 'Invalid argument(s)!'


if __name__ == '__main__':
    main()
