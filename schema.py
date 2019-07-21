import re

import marshmallow
from marshmallow import Schema
from marshmallow.validate import OneOf, Length


class CallRecordSchema(Schema):
    id = marshmallow.fields.Integer(dump_only=True)
    call_id = marshmallow.fields.Integer()
    type = marshmallow.fields.String(validate=OneOf(['start', 'end']))
    timestamp = marshmallow.fields.DateTime()
    source = marshmallow.fields.String(validate=Length(min=10, max=11))
    destination = marshmallow.fields.String(validate=Length(min=10, max=11))

    class Meta:
        strict = True

    @marshmallow.validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise marshmallow.ValidationError('Unknown field.', list(unknown))

    @marshmallow.pre_load
    def validate_phone_number(self, data):
        if data.get('source'):
            data['source'] = self.remove_non_numeric(data['source'])
        if data.get('destination'):
            data['destination'] = self.remove_non_numeric(data['destination'])
        return data

    @staticmethod
    def remove_non_numeric(phone):
        return re.sub('[^0-9]', '', phone)
