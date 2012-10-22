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


class WeeDB(object):

    def __init__(self):
        self._db = {}
        self._commands = ['SET', 'GET', 'UNSET', 'NUMEQUALTO', 'END', 'BEGIN',
                          'ROLLBACK', 'COMMIT']

    def parse_command(self, input_command):
        """Parse a command string and return a tuple of (command, [args]),
        where args is a list of arguments. If the command is invalid, raise an
        InvalidCommandError expcetion."""
        split = input_command.split()
        command = split[0]
        args = split[1:]

        if not self._is_valid_command(command):
            raise InvalidCommandError("Sorry, WeeDB doesn't know that one.")

    def _is_valid_command(self, command):
        """Return True if the command is valid, False otherwise. """
        if command.upper() in self._commands:
            return True
        else:
            return False


def main():
    db = WeeDB()
    try:
        db.parse_command('this is not valid ok')
    except InvalidCommandError:
        print 'Invalid command!'


if __name__ == '__main__':
    main()
