import datetime
import json
from unittest.mock import Mock

import pytest
from webtest import TestApp
import app


@pytest.fixture(scope='module')
def app_config():
    config = Mock(DATABASE_URL='sqlite://')
    return config


@pytest.fixture(scope='module')
def web_app(app_config):
    my_app = TestApp(app.wsgi_app(app_config))
    return my_app


@pytest.fixture
def start_call_payload():
    payload = {
        'id': 22,
        'call_id': 11,
        'type': 'start',
        'timestamp': str(datetime.datetime.utcnow()),
        'source': '48912345678',
        'destination': '4891234567',
    }
    return payload


def test_should_return_422_when_call_json_is_invalid(web_app, start_call_payload):
    start_call_payload['bad_key'] = 'i am bad'
    resp = web_app.post('/api/v1/register/call', json.dumps(start_call_payload),
                        content_type='application/json', status=422)
    assert resp.status_code == 422


def test_register_start_call(web_app, start_call_payload):
    resp = web_app.post('/api/v1/register/call', json.dumps(start_call_payload), content_type='application/json')
    assert resp.status_code == 201
