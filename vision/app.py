import os
from importlib import import_module

import bottle
import logging
import sys

from vision import db, tables
from vision.utils import env_detect
from vision.error import register_error_handler

os.chdir(os.path.dirname(__file__))
app = application = bottle.default_app()


def load_config():
    app.config.load_config('config/base.ini')

    cur_env = env_detect().lower()

    if os.path.exists('config/%s.ini' % cur_env):
        app.config.load_config('config/%s.ini' % cur_env)


def load_controllers():
    for path in ('vision.controllers', ):
        root_module = import_module(path)
        file_name = os.path.basename(root_module.__file__)
        if file_name != '__init__.py':
            continue

        root_dir = os.path.dirname(root_module.__file__)
        for c in os.listdir(root_dir):
            head, _ = os.path.splitext(c)
            if not head.startswith('_'):
                import_module(path + '.' + head)


def set_logger():
    default_format = ('[%(asctime)s] [%(levelname)s] '
                      '[%(module)s: %(lineno)d] %(message)s')
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format=default_format,
        datefmt='%Y-%m-%d %H:%M:%S %z',
    )


def install_plugins():
    from vision.plugins import boilerplate_plugin
    app.install(boilerplate_plugin)


def base_config():
    load_config()
    set_logger()
    db.init()
    tables.init()


def init_app():
    base_config()

    load_controllers()
    install_plugins()

    register_error_handler()

    return app
