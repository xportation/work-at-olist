import datetime

import dateutil
import marshmallow
import pytest

from schema import CallRecordSchema


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
    for t in ['start', 'end']:
        base_call_payload['type'] = t
        call_schema = CallRecordSchema()
        call_record, _ = call_schema.load(base_call_payload)
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


def test_should_remove_non_numeric_characters_from_phone_number(base_call_payload):
    base_call_payload['source'] = '(48) 99111-0000'
    base_call_payload['destination'] = '51 99010111'
    call_schema = CallRecordSchema()
    call_record, _ = call_schema.load(base_call_payload)
    assert call_record['source'] == '48991110000'
    assert call_record['destination'] == '5199010111'


def test_should_throws_when_phone_is_invalid(base_call_payload):
    base_call_payload['source'] = '(48) 99111-00002'
    base_call_payload['destination'] = '51 9901011'
    call_schema = CallRecordSchema()
    with pytest.raises(marshmallow.ValidationError) as e:
        _, _ = call_schema.load(base_call_payload)

    error_type = e.value.messages.get('source')
    assert len(error_type) >= 1
    # overkill assertion
    assert error_type[0] == 'Length must be between 10 and 11.'
    error_type = e.value.messages.get('destination')
    assert len(error_type) >= 1
    # overkill assertion
    assert error_type[0] == 'Length must be between 10 and 11.'


def test_should_accept_timestamp_in_iso_format(base_call_payload):
    base_call_payload['timestamp'] = '2019-01-16T23:22:34.000Z'
    call_schema = CallRecordSchema()
    call_record, _ = call_schema.load(base_call_payload)
    assert call_record['timestamp'] == datetime.datetime(2019, 1, 16, 23, 22, 34, 0, tzinfo=dateutil.tz.tzutc())
