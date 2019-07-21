import model


class CallService:
    def __init__(self, db):
        self.db = db

    def register_call(self, call_record):
        call_model = self.db.query(model.Call).filter_by(call_id=call_record['call_id']).first()
        if not call_model:
            call_model = model.Call()
        call_model.load_from_record(call_record)
        self.db.add(call_model)
        return call_model
