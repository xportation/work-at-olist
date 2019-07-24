import datetime

from sqlalchemy import and_

import model


class FareNotFoundException(Exception):
    def __init__(self, message):
        self.message = message


class InvalidBillingPeriod(Exception):
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

    @staticmethod
    def _define_billing_period(month, year):
        current_month = datetime.date.today().replace(day=1)
        if month and year:
            if month == current_month.month and year == current_month.year:
                raise InvalidBillingPeriod('The reference period is not ended yet.')
            else:
                current_month = datetime.date(year, month, 1)

        last_month = current_month - datetime.timedelta(days=1)
        last_month = last_month.replace(day=1)
        return last_month, current_month

    def billing_report(self, phone, month, year):
        first_day, first_day_next_month = self._define_billing_period(month, year)
        query = self.db.query(model.Call)
        query = query.filter(model.Call.origin_phone == phone)
        query = query.filter(and_(model.Call.end_timestamp >= first_day,
                                  model.Call.end_timestamp < first_day_next_month))
        calls = query.all()

        bills = []
        total_price = 0.0
        total_duration = datetime.timedelta()
        for call in calls:
            phone_bill = model.PhoneBill(call)
            duration = phone_bill.duration()
            price = phone_bill.price()
            total_price = total_price + price
            total_duration = total_duration + duration
            bills.append(phone_bill.report())
        return {
            'calls': bills, 'total_price': model.format_price(total_price),
            'total_duration': model.format_duration(total_duration)
        }
