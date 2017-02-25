from pycnic.core import Handler, WSGI
from pycnic.utils import requires_validation


def has_proper_name(data):
    if 'name' not in data or data['name'] != 'root':
        raise ValueError('Expected \'root\' as name')


class NameHandler(Handler):

    @requires_validation(has_proper_name)
    def post(self):
        return {'status': 'ok'}


class app(WSGI):
    routes = [('/name', NameHandler())]

if __name__ == "__main__":

    from wsgiref.simple_server import make_server
    try:
        print("Serving on 0.0.0.0:8080...")
        make_server('0.0.0.0', 8080, app).serve_forever()
    except KeyboardInterrupt:
        pass
    print("Done")
