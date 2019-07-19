import os

import bottle
from bottle_sqlalchemy import SQLAlchemyPlugin
from marshmallow import ValidationError
from sqlalchemy import create_engine

from config import Config
from schema import CallRecordSchema


def _r(data, status_code):
    bottle.response.status = status_code
    return data


@bottle.get('/')
def index():
    return '<h1 style="text-align: center;">Work at Olist</h1><h2 style="text-align: center;">Leonardo Vitor da Silva</h2><p style="text-align: center;"><a href="mailto:xportation@gmail.com">xportation@gmail.com</a></p>'


@bottle.post('/api/v1/register/call')
def register_call(db):
    call_schema = CallRecordSchema()
    _, _ = call_schema.load(bottle.request.json)
    return _r(bottle.request.json, 201)


def errors_handler_plugin(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            bottle.abort(422, str(e))
        except ValidationError as e:
            bottle.abort(422, e.messages)
    return wrapper


def wsgi_app(app_config):
    engine = create_engine(app_config.DATABASE_URL)

    app = bottle.default_app()
    app.install(errors_handler_plugin)
    app.install(SQLAlchemyPlugin(engine))
    return app


def main():
    try:
        port = int(os.environ.get('PORT', '5000'))
    except ValueError:
        port = 5000

    app_config = Config()
    bottle.run(app=wsgi_app(app_config), host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
