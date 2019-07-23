import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import model
import service
from service import ModelService


@pytest.fixture(scope='module')
def db():
    engine = create_engine('sqlite://')
    model.Base.metadata.create_all(bind=engine)
    create_session = sessionmaker()
    session = create_session(bind=engine)
    return session


@pytest.fixture(scope='module')
def db_fare(db):
    fare_model = model.Fare()
    fare_model.standing_charge = 0.36
    fare_model.call_minute_charge = 0.09
    fare_model.start_reduce_time = datetime.time(22, 0, 0, 0)
    fare_model.end_reduce_time = datetime.time(6, 0, 0, 0)
    fare_model.reduced_standing_charge = 0.32
    fare_model.reduced_call_minute_charge = 0.0
    fare_model.starts_at = datetime.datetime.utcnow()
    db.add(fare_model)
    db.commit()
    return db


def assert_start_end_values(call_model, start_call, end_call):
    assert call_model.call_id == start_call['call_id'] == end_call['call_id']
    assert call_model.origin_phone == start_call['source']
    assert call_model.destination_phone == start_call['destination']
    assert call_model.start_timestamp == start_call['timestamp']
    assert call_model.end_timestamp == end_call['timestamp']


def test_register_call_throws_fare_not_found_if_there_is_not_fare_registered(db, start_call):
    with pytest.raises(service.FareNotFoundException):
        model_service = ModelService(db)
        model_service.register_call(start_call)


def test_register_start_call(db_fare, start_call):
    model_service = ModelService(db_fare)
    call_model = model_service.register_call(start_call)
    db_fare.commit()
    call_from_db = db_fare.query(model.Call).filter_by(call_id=call_model.call_id).first()
    assert call_model.origin_phone == call_from_db.origin_phone
    assert call_model.destination_phone == call_from_db.destination_phone


def test_register_end_call(db_fare, end_call):
    model_service = ModelService(db_fare)
    call_model = model_service.register_call(end_call)
    db_fare.commit()
    call_from_db = db_fare.query(model.Call).filter_by(call_id=call_model.call_id).first()
    assert call_model.end_timestamp == call_from_db.end_timestamp


def test_should_keep_same_db_id_when_create_start_and_end_call_in_sequence(db_fare, start_call, end_call):
    end_call['call_id'] = start_call['call_id']
    model_service = ModelService(db_fare)
    start_call_model = model_service.register_call(start_call)
    db_fare.commit()
    end_call_model = model_service.register_call(end_call)
    db_fare.commit()
    call_from_db = db_fare.query(model.Call).filter_by(call_id=start_call['call_id']).first()
    assert call_from_db.id == start_call_model.id == end_call_model.id
    assert call_from_db.call_id == start_call_model.call_id == end_call_model.call_id
    assert_start_end_values(call_from_db, start_call, end_call)


def test_should_keep_same_db_id_when_create_end_and_start_call_in_sequence(db_fare, start_call, end_call):
    end_call['call_id'] = start_call['call_id']
    model_service = ModelService(db_fare)
    end_call_model = model_service.register_call(end_call)
    db_fare.commit()
    start_call_model = model_service.register_call(start_call)
    db_fare.commit()
    call_from_db = db_fare.query(model.Call).filter_by(call_id=start_call['call_id']).first()
    assert call_from_db.id == start_call_model.id == end_call_model.id
    assert call_from_db.call_id == start_call_model.call_id == end_call_model.call_id
    assert_start_end_values(call_from_db, start_call, end_call)
