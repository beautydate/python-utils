#!/usr/bin/python
# coding: utf-8
"""MySQLdb Cursors

This module implements Cursors of various types for MySQLdb. By
default, MySQLdb uses the Cursor class.

Changed by Navegg - <it@navegg.com>"""

from MySQLdb.cursors import *
from _mysql_exceptions import (MySQLError, Warning, Error, InterfaceError,
                               DatabaseError, DataError, OperationalError,
                               IntegrityError, InternalError, ProgrammingError,
                               NotSupportedError)


def try_reconnect(obj, **kwargs):

    import time
    from navegg_utils import connections

    count = 3
    msg = ''
    while count > 0:
        try:
            return connections.Connection(**kwargs)
        except (MySQLError, Warning, Error, InterfaceError,
                DatabaseError, DataError, OperationalError, IntegrityError,
                InternalError, ProgrammingError, NotSupportedError) as ex:

            code = ex[0]
            msg = ex[1]
            time.sleep(1)
            count -= 1

    raise Exception(code, "Were executed 3 attempt to connect without success: * %s * " % msg)


class SafeExecute(object):

    def __call__(self, fn):

        def do_safe(self, *args, **kwargs):
            try:
                fn(self, *args, **kwargs)
            except (MySQLError, Warning, Error, InterfaceError,
                    DatabaseError, DataError, OperationalError, IntegrityError,
                    InternalError, ProgrammingError, NotSupportedError) as ex:
                print ex.args
                if ex.args[0] in [1203, 2002, 2006, 2013, 2014, 2045, 2055]:
                    kw = {'host': self.connection.host,
                          'user': self.connection.user,
                          'passwd': self.connection.passwd,
                          'port': self.connection.port,
                          'charset': self.connection.charset,
                          'db': self.connection.db}
                    self.connection.close()
                    del self.connection
                    self.connection = try_reconnect(self, **kw)
                else:
                    raise

        return do_safe


class NaveggBaseCursor(BaseCursor):

    @SafeExecute()
    def execute(self, query, args=None):
        return super(NaveggBaseCursor, self).execute(query, args)

    @SafeExecute()
    def executemany(self, query, args):
        return super(NaveggBaseCursor, self).executemany(query, args)


class Cursor(CursorStoreResultMixIn, CursorTupleRowsMixIn,
             NaveggBaseCursor):

    """This is the standard Cursor class that returns rows as tuples
    and stores the result set in the client.

    Changed by Navegg - <it@navegg.com>"""


class DictCursor(CursorStoreResultMixIn, CursorDictRowsMixIn,
                 NaveggBaseCursor):

    """This is a Cursor class that returns rows as dictionaries and
    stores the result set in the client.

    Changed by Navegg - <it@navegg.com>"""


class SSCursor(CursorUseResultMixIn, CursorTupleRowsMixIn,
               NaveggBaseCursor):

    """This is a Cursor class that returns rows as tuples and stores
    the result set in the server.

    Changed by Navegg - <it@navegg.com>"""


class SSDictCursor(CursorUseResultMixIn, CursorDictRowsMixIn,
                   NaveggBaseCursor):

    """This is a Cursor class that returns rows as dictionaries and
    stores the result set in the server.

    Changed by Navegg - <it@navegg.com>"""
