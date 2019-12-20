from marshmallow import Schema, fields


class StorageSerializer(Schema):
    id = fields.Int(as_string=True)
    content_type = fields.Str()
    path = fields.Str()
    is_valid = fields.Bool()
    size = fields.Int()
    created_at = fields.DateTime('%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%d %H:%M:%S')


storage_serializer = StorageSerializer(strict=True)
