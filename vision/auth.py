from datetime import datetime

import bottle
import peewee
import logging
from bottle import request

app = bottle.default_app()


def get_api_user():
    """
    这里处理用户鉴权逻辑
    """
    token, _ = request.auth or (None, None)
    if token is None:
        return
    else:
        return True


def get_api_user_or_401():
    user = get_api_user()
    if user is None:
        headers = {'WWW-Authenticate': 'Basic realm="vision"'}
        raise bottle.HTTPError(401, 'Authorization required', **headers)


def check_api_user():
    get_api_user_or_401()
