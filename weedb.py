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
        # each of these commands maps to one of WeeDB's methods
        self._commands = { 'SET': self._set,
                           'GET': self._get,
                           'UNSET': self._unset,
                           'NUMEQUALTO': self._numequalto,
                           'END': self._end,
                           'BEGIN': self._begin,
                           'ROLLBACK': self._rollback,
                           'COMMIT': self._commit }

        # self._db is a handle for the "real" database, which is also the first
        # element in the self._transactions list. As new transactional blocks
        # are opened, new dictionaries are appended to self._transactions. As
        # they're rolled back or committed, they're either popped off or
        # flattened down, respectively.
        self._db = {}
        self._transactions = [self._db]

    def execute_command(self, input_command):
        """Parse and execute a database command, passed as a string. Raises
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
        """Set name to value."""
        # always set to newest transactional block, if one exists
        self._transactions[-1][name] = value

    def _get(self, name):
        """Print value of name. Print NULL if name isn't set."""
        flattened = self._flatten_transaction_layers()
        value = flattened.get(name)
        if value:
            print value
        else:
            print 'NULL'

    def _unset(self, name):
        """Remove name from database."""
        if self._uncommitted_transactions():
            # can't just delete here, since we have to be able to roll back
            self._transactions[-1][name] = None
        else:
            del self._db[name]

    def _numequalto(self, value):
        """Print number of entries with the given value."""
        flattened = self._flatten_transaction_layers()
        n = [name for name, val in flattened.iteritems() if val == value]
        print len(n)

    def _end(self):
        """Exit the interactive database."""
        sys.exit(0)

    def _begin(self):
        """Open a transactional block."""
        self._transactions.append({})

    def _rollback(self):
        """Rollback all commands from most recent transactional block."""
        if self._uncommitted_transactions():
            self._transactions.pop()
        else:
            print "INVALID ROLLBACK"

    def _commit(self):
        """Permanently store all operations from any open transactional
        block."""
        self._transactions = [ self._flatten_transaction_layers() ]
        # TODO: delete names whose values are None at this point

    def _uncommitted_transactions(self):
        """Return True if there are pending transactions, False otherwise."""
        if len(self._transactions) > 1:
            return True
        else:
            return False

    def _flatten_transaction_layers(self):
        """Merge all transaction blocks into a single dictionary, giving
        precedence to the most recent. Gettin' a little functional here. Note
        use of reversed() to make it a right fold."""
        return reduce(self._merge_dictionaries, reversed(self._transactions))

    def _merge_dictionaries(self, x, y):
        """Helper function to be called by reduce(), used to fold together a
        list of dictionaries. Turns two dictionaries into one by assigning all
        of x's values to y, overwriting where necessary."""
        return dict(y.items() + x.items())


def main():
    """My main() man."""
    db = WeeDB()

    print 'Welcome to WeeDB. Have a tiny bit of fun!'
    while True:
        try:
            command = raw_input('>>> ')
        except (KeyboardInterrupt, EOFError):
            sys.exit(0)

        try:
            db.execute_command(command)
        except InvalidCommandError:
            print "Sorry, I don't know that command!"
        except InvalidArgumentError:
            print 'Invalid argument(s)!'


if __name__ == '__main__':
    main()
