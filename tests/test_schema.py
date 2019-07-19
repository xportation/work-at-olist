import datetime

import marshmallow
import pytest

from schema import CallRecordSchema


@pytest.fixture
def base_call_payload():
    payload = {
        'id': 22,
        'call_id': 11,
        'type': 'start',
        'timestamp': str(datetime.datetime.utcnow()),
    }
    return payload


def test_should_throws_when_call_record_type_is_not_start_or_end(base_call_payload):
    base_call_payload['type'] = 'started'
    call_schema = CallRecordSchema()
    with pytest.raises(marshmallow.ValidationError) as e:
        _, _ = call_schema.load(base_call_payload)

    error_type = e.value.messages.get('type')
    assert len(error_type) >= 1
    # overkill assertion
    assert error_type[0] == 'Not a valid choice.'


def test_should_accept_call_record_type_when_is_start_or_end(base_call_payload):
    for type in ['start', 'end']:
        base_call_payload['type'] = type
        call_schema = CallRecordSchema()
        call_record, _ = call_schema.load(base_call_payload)
        assert call_record['id'] == 22
        assert call_record['call_id'] == 11


def test_should_throws_when_data_has_unknown_fields(base_call_payload):
    additional_fields = ['start_timestamp', 'origin_phone', 'end_timestamp', 'destination_phone', 'miau']
    for field in additional_fields:
        base_call_payload[field] = 'my_value'

    call_schema = CallRecordSchema()
    with pytest.raises(marshmallow.ValidationError) as e:
        _, _ = call_schema.load(base_call_payload)

    for field in additional_fields:
        error_type = e.value.messages.get(field)
        assert len(error_type) >= 1
