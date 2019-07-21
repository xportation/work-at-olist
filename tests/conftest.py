import datetime

import marshmallow
import pytest


@pytest.fixture
def base_call_payload():
    payload = {
        'call_id': 11,
        'type': 'start',
        'timestamp': marshmallow.utils.isoformat(datetime.datetime.utcnow()),
    }
    return payload


@pytest.fixture
def start_call_payload(base_call_payload):
    base_call_payload['source'] = '48912345678'
    base_call_payload['destination'] = '4891234567'
    return base_call_payload


@pytest.fixture
def start_call():
    call_record = {
        'call_id': 11,
        'type': 'start',
        'timestamp': datetime.datetime.utcnow(),
        'source': '48912345678',
        'destination': '4891234567'
    }
    return call_record


@pytest.fixture
def end_call():
    call_record = {
        'call_id': 13,
        'type': 'end',
        'timestamp': datetime.datetime.utcnow()
    }
    return call_record
