import os

import bottle


@bottle.route('/', method='GET')
def index():
    return '<h1 style="text-align: center;">Work at Olist</h1><h2 style="text-align: center;">Leonardo Vitor da Silva</h2><p style="text-align: center;"><a href="mailto:xportation@gmail.com">xportation@gmail.com</a></p>'


def wsgi_app():
    return bottle.default_app()


if __name__ == '__main__':
    try:
        PORT = int(os.environ.get('PORT', '5000'))
    except ValueError:
        PORT = 5000

    bottle.run(app=wsgi_app(), host='0.0.0.0', port=PORT)
