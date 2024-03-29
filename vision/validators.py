from collections import defaultdict

from voluptuous import (
    message,
    TrueInvalid,
    truth,
    Schema,
    re,
    Coerce,
    REMOVE_EXTRA,
)


class ValidatorSchema(Schema):
    def update(self, schema, required=None, extra=None):
        """ 类似 extend，但是会覆盖掉 repr 相同的 key """
        assert type(self.schema) == dict and type(schema) == dict

        result = self.schema.copy()

        result_key_map = defaultdict(list)
        for rk in result:
            result_key_map[str(rk)].append(rk)
        for sk in schema:
            for rk in result_key_map[str(sk)]:
                result.pop(rk)

        result.update(schema)

        result_required = (required if required is not None else self.required)
        result_extra = (extra if extra is not None else self.extra)
        return Schema(result, required=result_required, extra=result_extra)

    def replace_keys(self, *keys):
        assert type(self.schema) == dict, 'Schemas must be dictionary-based'

        result = self.schema.copy()

        result_key_map = defaultdict(list)
        for rk in result:
            result_key_map[str(rk)].append(rk)
        for sk in keys:
            for rk in result_key_map[str(sk)]:
                result[sk] = result.pop(rk)

        return Schema(result, required=self.required, extra=self.extra)


storage_query_validator = ValidatorSchema(
    {
        'user_id': Coerce(int),
        'type': Coerce(int),
    }, extra=REMOVE_EXTRA)
