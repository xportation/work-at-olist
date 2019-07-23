import json
from unittest import mock

import pytest
import sqlalchemy
from webtest import TestApp

import app
import model


@pytest.fixture(scope='module')
def my_engine():
    engine = sqlalchemy.create_engine('sqlite://')
    model.Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope='module')
def web_app(my_engine):
    my_app = TestApp(app.wsgi_app(my_engine))
    return my_app


def test_should_return_422_when_call_json_is_invalid(web_app, start_call_payload):
    start_call_payload['bad_key'] = 'i am bad'
    resp = web_app.post('/api/v1/calls', json.dumps(start_call_payload),
                        content_type='application/json', status=422)
    assert resp.status_code == 422


def test_register_call_fail_if_there_no_fare_registered(web_app, start_call_payload):
    resp = web_app.post('/api/v1/calls', json.dumps(start_call_payload),
                        content_type='application/json', status=422)
    assert resp.status_code == 422


def test_register_fare(web_app, fare_payload):
    resp = web_app.post('/api/v1/fares', json.dumps(fare_payload), content_type='application/json')
    assert resp.status_code == 201


def test_register_start_call(web_app, start_call_payload, fare_payload):
    _ = web_app.post('/api/v1/fares', json.dumps(fare_payload), content_type='application/json')
    resp = web_app.post('/api/v1/calls', json.dumps(start_call_payload), content_type='application/json')
    assert resp.status_code == 201