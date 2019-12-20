import logging

from vision import models
from vision.models import (ModelBase, get_ordered_models)


def init():
    #建表
    ordered_models = get_ordered_models(models)

    try:
        for model in ordered_models:
            if model != ModelBase:
                model.create_table()

    except Exception as e:
        logging.error(e)
