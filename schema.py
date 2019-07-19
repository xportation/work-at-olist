import marshmallow
from marshmallow import Schema
from marshmallow.validate import OneOf, Length


class CallRecordSchema(Schema):
    id = marshmallow.fields.Integer()
    call_id = marshmallow.fields.Integer()
    type = marshmallow.fields.String(validate=OneOf(['start', 'end']))
    timestamp = marshmallow.fields.DateTime()
    source = marshmallow.fields.String(validate=Length(min=10))
    destination = marshmallow.fields.String(validate=Length(min=10))

    class Meta:
        strict = True

    @marshmallow.validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise marshmallow.ValidationError('Unknown field.', list(unknown))
