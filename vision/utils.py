import os
from datetime import datetime, date
from enum import Enum

import re

import sys
from bottle import request
from decimal import Decimal

from vision import snowflake


def _plain_args(d, list_fields=None):
    list_fields = list_fields or ()

    result = dict((key, d.getunicode(key).strip()) for key in d)
    for key in list_fields:
        result[key] = [v.strip() for v in d.getall(key)]

    return result


def plain_forms(list_fields=None):
    """ Plain POST data. """
    return _plain_args(request.forms, list_fields)


def plain_query(list_fields=None):
    """ Plain GET data """
    return _plain_args(request.query, list_fields)


def plain_params(list_fields=None):
    """ Plain all data """
    return _plain_args(request.params, list_fields)


id_generator = snowflake.generator(1, 1)


def idg():
    return next(id_generator)


def env_detect():
    env = os.environ.get('APP_ENV')
    if env is None:
        test_commands = ('utrunner.py', 'nose', 'nose2', 'pytest')
        if os.path.basename(sys.argv[0]) in test_commands:
            env = 'TESTING'
        else:
            env = 'DEV'
    return env
