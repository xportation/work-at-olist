import model


def test_should_load_start_timestamp_when_type_is_start(start_call):
    call_model = model.Call()
    call_model.load_from_record(start_call)
    assert call_model.start_timestamp == start_call['timestamp']


def test_should_load_end_timestamp_when_type_is_end(end_call):
    call_model = model.Call()
    call_model.load_from_record(end_call)
    assert call_model.end_timestamp == end_call['timestamp']
