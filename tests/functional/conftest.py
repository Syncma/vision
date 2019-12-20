from base64 import b64encode

import pytest
from ..helper import TestApp, drop_and_create_database

from vision import models
from vision.models import (
    ModelBase,
    get_ordered_models,
    QiniuStorage,
)
from vision.utils import idg
from vision.app import init_app


@pytest.fixture(scope='session')
def app():
    return TestApp(init_app())


@pytest.fixture(autouse=True, scope='session')
def db(app):
    """初始化数据库，只会执行一次"""
    c = app.app.config
    print("app.app.config=", c)
    drop_and_create_database(app.app.config)

    # 重建表
    ordered_models = get_ordered_models(models)

    for model in ordered_models:
        if model != ModelBase:
            model.create_table()


@pytest.fixture
def auth_header(request):
    val = "1234"
    val = b64encode(val.encode('utf-8')).strip()
    val = val.decode('latin1')

    header = {
        'Authorization': 'Basic ' + val,
    }
    return header


@pytest.fixture
def storages(request):
    insert = [
        {
            'content_type': 'image/jpeg',
            'path': '/home',
            'is_valid': True,
        },
        {
            'content_type': 'image/jpeg',
            'path': '/home',
            'is_valid': True,
        },
        {
            'content_type': 'image/jpeg',
            'path': '/home',
            'is_valid': True,
        },
        {
            'content_type': 'image/jpeg',
            'path': '/home',
            'is_valid': True,
        },
    ]
    _storage = []
    for _ins in insert:
        _storage.append(QiniuStorage.create(**_ins))

    def teardown():
        for _del in _storage:
            _del.delete_instance()

    request.addfinalizer(teardown)
    return _storage
