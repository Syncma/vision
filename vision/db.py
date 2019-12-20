import os
import bottle

from bottle import hook
from peewee import MySQLDatabase
from playhouse.pool import PooledMySQLDatabase


class BeginPooledMySQL(PooledMySQLDatabase):
    def begin(self):
        # db api 并没有自动加 begin 语句，所以在此要手动加上
        self.get_conn().begin()


class BeginMySQLDatabase(MySQLDatabase):
    def begin(self):
        # db api 并没有自动加 begin 语句，所以在此要手动加上
        self.get_conn().begin()


db = BeginMySQLDatabase(None, autocommit=False)


def init():
    app = bottle.default_app()

    app.config.setdefault('db.read_timeout', 20)
    app.config.setdefault('db.write_timeout', 20)
    db_password = os.environ.get('DB_PASSWORD') or app.config['db.password']

    db.init(
        app.config['db.database'],
        host=app.config['db.host'],
        user=app.config['db.user'],
        port=int(app.config['db.port']),
        charset=app.config['db.charset'],
        password=db_password,
        autocommit=True,  # 连接mysql 时是否使用autocommit 模式
        read_timeout=app.config['db.read_timeout'],
        write_timeout=app.config['db.write_timeout'],
    )


@hook('before_request')
def _connect_db():
    db.get_conn()


@hook('after_request')
def _close_db():
    if not db.is_closed():
        db.close()
