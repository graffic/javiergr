"""
ZODB support in flask

Usage: `DB = FlaskZODB(APP)`

In your views use `DB.root` to get the database root dictionary.
"""
from flask import _app_ctx_stack as stack
import transaction
import zodburi
from ZODB import DB


class FlaskZODB(object):
    """ZODB database manager for Flask"""
    def __init__(self, app):
        self.__db = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initializes the ZODB database with an app"""
        app.config.setdefault('ZODB_URI', 'memory://')
        app.teardown_appcontext(_close_connection)
        if self.__db is not None:
            self.__db.close()
        self.__db = _initialize_database(app)

    @property
    def connection(self):
        """Gets a connection in the current context (opens it if needed)"""
        ctx = stack.top
        if ctx is None:
            return

        conn = getattr(ctx, 'zodb_conn', None)
        if conn is not None:
            return conn

        ctx.zodb_conn = self.__db.open()
        return ctx.zodb_conn

    @property
    def root(self):
        """Database root"""
        return self.connection.root()


def _close_connection(exception):
    """Close the current connection in the top context"""
    ctx = stack.top
    conn = getattr(ctx, 'zodb_conn', None)
    if conn is None:
        return

    if exception is not None or transaction.isDoomed():
        transaction.abort()
    else:
        transaction.commit()
    conn.close()


def _initialize_database(app):
    """Main connection to the database"""
    uri = app.config['ZODB_URI']
    storage_factory, dbkw = zodburi.resolve_uri(uri)
    return DB(storage_factory(), **dbkw)
