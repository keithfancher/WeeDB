#!/usr/bin/env python


# Copyright 2012 Keith Fancher
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


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
        if not self._is_valid_command(command):
            raise InvalidCommandError("Sorry, WeeDB doesn't know that one.")
        try:
            self._commands[command](*args)
        except TypeError:
            raise InvalidArgumentError('Invalid argument(s)!')

    def _parse_command(self, command):
        """Parse a command string and return a tuple of (command, [args]),
        where args is a list of arguments."""
        com_list = command.split()
        return (com_list[0].upper(), com_list[1:])

    def _is_valid_command(self, command):
        """Return True if the command is valid, False otherwise. """
        if command.upper() in self._commands.keys():
            return True
        else:
            return False

    def _set(self, name, value):
        print 'set ' + name + ' ' + value

    def _get(self, name):
        print 'get ' + name

    def _unset(self, name):
        print 'unset ' + name

    def _numequalto(self, value):
        print 'numequalto ' + value

    def _end(self):
        print 'end'

    def _begin(self):
        print 'begin'

    def _rollback(self):
        print 'rollback'

    def _commit(self):
        print 'commit'


def main():
    db = WeeDB()
    try:
        db.execute_command('SET a 10')
        db.execute_command('GET a')
        db.execute_command('UNSET a')
        db.execute_command('NUMEQUALTO 10')
        db.execute_command('BEGIN')
        db.execute_command('ROLLBACK')
        db.execute_command('COMMIT')
        db.execute_command('END')
        db.execute_command('BLARG')
    except InvalidCommandError:
        print 'Invalid command!'
    except InvalidArgumentError:
        print 'Invalid argument(s)!'


if __name__ == '__main__':
    main()
