# import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import model
from service import CallService


@pytest.fixture(scope='module')
def db():
    engine = create_engine('sqlite://')
    model.Base.metadata.create_all(bind=engine)
    create_session = sessionmaker()
    session = create_session(bind=engine)
    return session


def assert_start_end_values(call_model, start_call, end_call):
    assert call_model.call_id == start_call['call_id'] == end_call['call_id']
    assert call_model.origin_phone == start_call['source']
    assert call_model.destination_phone == start_call['destination']
    assert call_model.start_timestamp == start_call['timestamp']
    assert call_model.end_timestamp == end_call['timestamp']


def test_register_start_call(db, start_call):
    call_service = CallService(db)
    call_model = call_service.register_call(start_call)
    db.commit()
    call_from_db = db.query(model.Call).filter_by(call_id=call_model.call_id).first()
    assert call_model.origin_phone == call_from_db.origin_phone
    assert call_model.destination_phone == call_from_db.destination_phone


def test_register_end_call(db, end_call):
    call_service = CallService(db)
    call_model = call_service.register_call(end_call)
    db.commit()
    call_from_db = db.query(model.Call).filter_by(call_id=call_model.call_id).first()
    assert call_model.end_timestamp == call_from_db.end_timestamp


def test_should_keep_same_db_id_when_create_start_and_end_call_in_sequence(db, start_call, end_call):
    end_call['call_id'] = start_call['call_id']
    call_service = CallService(db)
    start_call_model = call_service.register_call(start_call)
    db.commit()
    end_call_model = call_service.register_call(end_call)
    db.commit()
    call_from_db = db.query(model.Call).filter_by(call_id=start_call['call_id']).first()
    assert call_from_db.id == start_call_model.id == end_call_model.id
    assert call_from_db.call_id == start_call_model.call_id == end_call_model.call_id
    assert_start_end_values(call_from_db, start_call, end_call)


def test_should_keep_same_db_id_when_create_end_and_start_call_in_sequence(db, start_call, end_call):
    end_call['call_id'] = start_call['call_id']
    call_service = CallService(db)
    end_call_model = call_service.register_call(end_call)
    db.commit()
    start_call_model = call_service.register_call(start_call)
    db.commit()
    call_from_db = db.query(model.Call).filter_by(call_id=start_call['call_id']).first()
    assert call_from_db.id == start_call_model.id == end_call_model.id
    assert call_from_db.call_id == start_call_model.call_id == end_call_model.call_id
    assert_start_end_values(call_from_db, start_call, end_call)
