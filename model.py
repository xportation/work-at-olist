from sqlalchemy import Column, Integer, String, DateTime, Float, Time, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


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
