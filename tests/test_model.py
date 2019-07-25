import datetime

import pytest

import model


def test_should_load_start_timestamp_when_type_is_start(start_call):
    call_model = model.Call()
    call_model.load_from_record(start_call)
    assert call_model.start_timestamp == start_call['timestamp']


def test_should_load_end_timestamp_when_type_is_end(end_call):
    call_model = model.Call()
    call_model.load_from_record(end_call)
    assert call_model.end_timestamp == end_call['timestamp']


def test_get_charges(fare_model):
    expectations = [
        (datetime.time(22, 0, 0), 0.5, 0.05),
        (datetime.time(5, 59, 59), 0.5, 0.05),
        (datetime.time(23, 59, 0), 0.5, 0.05),
        (datetime.time(0, 0, 0), 0.5, 0.05),
        (datetime.time(0, 1, 0), 0.5, 0.05),
        (datetime.time(4, 15, 44), 0.5, 0.05),
        (datetime.time(21, 59, 59), 1.1, 0.1),
        (datetime.time(6, 0, 0), 1.1, 0.1),
        (datetime.time(10, 14, 0), 1.1, 0.1),
    ]
    for time, charge, minute_charge in expectations:
        c, m = fare_model.get_charges(time)
        assert charge == pytest.approx(c, 0.0001)
        assert minute_charge == pytest.approx(m, 0.0001)


def test_phone_bill_report(call_model, fare_model):
    call_model.fare = fare_model
    phone_bill_model = model.PhoneBill(call_model)
    report = phone_bill_model.report()
    assert report['destination'] == '99900900909'
    assert report['start_date'] == datetime.date(1984, 2, 18)
    assert report['start_time'] == datetime.time(20, 5, 44)
    assert report['duration'] == '00h02m18s'
    assert report['price'] == 'R$ 1.30'


def test_format_duration_when_have_days():
    duration = datetime.timedelta(days=5.0, hours=23.0, minutes=12.0, seconds=4.0)
    duration_str = model.format_duration(duration)
    assert duration_str == '143h12m04s'
