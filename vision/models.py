import inspect

from peewee import (
    Model,
    R,
    DateTimeField,
    CharField,
    BigIntegerField,
    DoesNotExist,
    TextField,
    IntegerField,
    BooleanField,
)

from vision.db import db
from vision.utils import idg, ChoiceEnum


def get_ordered_models(module):
    """ 按代码出现的先后顺序获取某一 module 中所有的 peewee.Model 子类 """

    def is_model(m):
        return isinstance(m, type) and issubclass(m, Model) and m != Model

    members = inspect.getmembers(module, is_model)
    # 按代码中的先后顺序排序
    members.sort(key=lambda x: inspect.getsourcelines(x[1])[1])
    return [model for _, model in members]


class ModelBase(Model):
    created_at = DateTimeField(constraints=[R('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(constraints=[
        R('DEFAULT CURRENT_TIMESTAMP'),
        R('ON UPDATE CURRENT_TIMESTAMP')
    ])

    @classmethod
    def get_or_none(cls, *query, **kwargs):
        """
        :rtype: ModelBase
        """
        try:
            return cls.get(*query, **kwargs)
        except DoesNotExist:
            return None

    def update_dict(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    class Meta:
        database = db
        only_save_dirty = True


class QiniuStorage(ModelBase):
    id = BigIntegerField(default=idg, primary_key=True)
    content_type = CharField(max_length=32)
    path = CharField(max_length=128)
    is_valid = BooleanField(default=False)
    size = IntegerField(default=0)

    class Meta:
        db_table = 'storage'

    def full_url(self):
        return self.path
