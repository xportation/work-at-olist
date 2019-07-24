import json
import os

import bottle
from bottle_sqlalchemy import SQLAlchemyPlugin
from marshmallow import ValidationError
from sqlalchemy import create_engine

import schema
from config import Config
from schema import CallRecordSchema, FareSchema, PhoneBillSchema
from service import ModelService, FareNotFoundException, InvalidBillingPeriod


def _r(data, status_code):
    bottle.response.status = status_code
    return data


@bottle.get('/')
def index():
    return '<h1 style="text-align: center;">Work at Olist</h1><h2 style="text-align: center;">Leonardo Vitor da Silva</h2><p style="text-align: center;"><a href="mailto:xportation@gmail.com">xportation@gmail.com</a></p>'


@bottle.post('/api/v1/calls')
def register_call(db):
    call_schema = CallRecordSchema()
    call_record, _ = call_schema.load(bottle.request.json)
    model_service = ModelService(db)
    model_service.register_call(call_record)
    _return_call, _ = call_schema.dump(call_record)
    return _r(_return_call, 201)


@bottle.post('/api/v1/fares')
def register_fare(db):
    fare_schema = FareSchema()
    fare_model, _ = fare_schema.load(bottle.request.json)
    db.add(fare_model)
    _return_fare, _ = fare_schema.dump(fare_model)
    return _r(_return_fare, 201)


@bottle.get('/api/v1/bills/<phone>')
def load_bills(db, phone):
    phone = schema.remove_non_numeric(phone)
    args = bottle.request.query
    month = int(args.month) if args.month else None
    year = int(args.year) if args.year else None

    model_service = ModelService(db)
    billing = model_service.billing_report(phone, month, year)

    phone_bill_schema = PhoneBillSchema()
    _return_billing, _ = phone_bill_schema.dump(billing)
    return _r(_return_billing, 200)


def error_callback(error_context):
    return json.dumps(dict(message=error_context.body))


error_handler_callback = {
    404: error_callback,
    422: error_callback,
    500: error_callback
}


def errors_handler_plugin(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            bottle.abort(422, str(e))
        except ValidationError as e:
            bottle.abort(422, e.messages)
        except FareNotFoundException as e:
            bottle.abort(422, str(e))
        except InvalidBillingPeriod as e:
            bottle.abort(404, str(e))
    return wrapper


def wsgi_app(engine):
    app = bottle.default_app()
    app.error_handler = error_handler_callback
    app.install(errors_handler_plugin)
    app.install(SQLAlchemyPlugin(engine))
    return app


def main():
    try:
        port = int(os.environ.get('PORT', '5000'))
    except ValueError:
        port = 5000

    app_config = Config()
    engine = create_engine(app_config.DATABASE_URL)
    bottle.run(app=wsgi_app(engine), host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
