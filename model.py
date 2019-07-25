import datetime
import math

from sqlalchemy import Column, Integer, String, DateTime, Float, Time, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def format_duration(duration):
    t = datetime.datetime.utcfromtimestamp(duration.total_seconds())
    return t.strftime("%Hh%Mm%Ss")


def format_price(price):
    return f'R$ {price:.2f}'


class Fare(Base):
    __tablename__ = 'fare'

    id = Column(Integer, primary_key=True, autoincrement=True)
    standing_charge = Column(Float(precision=2), nullable=False)
    call_minute_charge = Column(Float(precision=2), nullable=False)
    start_reduce_time = Column(Time, nullable=False)
    end_reduce_time = Column(Time, nullable=False)
    reduced_standing_charge = Column(Float(precision=2), nullable=False)
    reduced_call_minute_charge = Column(Float(precision=2), nullable=False)
    starts_at = Column(DateTime, nullable=False, default=func.now())

    def get_charges(self, timestamp):
        """
        Define the standing and minute charge. The fare varies by the reduce time
        :param timestamp:
        :return: tuple of standing and minute charge
        """

        def time_in_reduce_period(start, end):
            if start <= end:
                return start <= timestamp < end
            else:
                return start <= timestamp or timestamp < end

        if time_in_reduce_period(self.start_reduce_time, self.end_reduce_time):
            return self.reduced_standing_charge, self.reduced_call_minute_charge
        return self.standing_charge, self.call_minute_charge


class Call(Base):
    __tablename__ = 'call'

    id = Column(Integer, primary_key=True, autoincrement=True)
    call_id = Column(Integer, unique=True, nullable=False)
    start_timestamp = Column(DateTime, nullable=True)
    origin_phone = Column(String(11), nullable=True)
    destination_phone = Column(String(11), nullable=True)
    end_timestamp = Column(DateTime, nullable=True)
    fare_id = Column(Integer, ForeignKey('fare.id'), nullable=False)
    fare = relationship('Fare')

    def load_from_record(self, call_record):
        """
        Load call data from dict
        The start and end timestamp is defined by the key: type.
        Keys:
          - call_id
          - type: start or end
          - timestamp
          - source
          - destination
        :param call_record: dict
        """
        self.call_id = call_record['call_id']
        if self.is_start(call_record):
            self.start_timestamp = call_record['timestamp']
            self.origin_phone = call_record['source']
            self.destination_phone = call_record['destination']
        else:
            self.end_timestamp = call_record['timestamp']

    @staticmethod
    def is_start(call_record):
        return call_record['type'] == 'start'


class PhoneBill:
    def __init__(self, call):
        self.call = call

    def report(self):
        """
        :return: dict
            - destination
            - start_date
            - start_time
            - duration (hour, minute and seconds): e.g. 0h35m42s
            - price: e.g. R$ 3.96
        """
        price = self.price()
        duration = self.duration()
        return {
            'destination': self.call.destination_phone, 'start_date': self.call.start_timestamp.date(),
            'start_time': self.call.start_timestamp.time(), 'duration': format_duration(duration),
            'price': format_price(price)
        }

    def duration(self):
        return self.call.end_timestamp - self.call.start_timestamp

    def price(self):
        duration = self.duration()
        minutes = math.trunc(duration.total_seconds() / 60.0)
        standing_charge, minute_charge = self.call.fare.get_charges(self.call.start_timestamp.time())
        return standing_charge + minutes * minute_charge
