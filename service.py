import datetime

import model


class FareNotFoundException(Exception):
    def __init__(self, message):
        self.message = message


class ModelService:
    def __init__(self, db):
        self.db = db

    def register_call(self, call_record):
        call_model = self.db.query(model.Call).filter_by(call_id=call_record['call_id']).first()
        if not call_model:
            call_model = model.Call()
            call_model.fare = self.load_current_fare()
        call_model.load_from_record(call_record)
        self.db.add(call_model)
        return call_model

    def load_current_fare(self):
        fare_model = self.db.query(model.Fare).\
            filter(model.Fare.starts_at <= datetime.datetime.utcnow()).\
            order_by(model.Fare.starts_at.desc()).limit(1).first()
        if not fare_model:
            raise FareNotFoundException('Fare not found.')
        return fare_model
