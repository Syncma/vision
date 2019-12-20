import bottle
from bottle import get

app = bottle.default_app()


@get('/')
def index():
    pass  # health check
