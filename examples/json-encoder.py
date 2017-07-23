#!/usr/bin/env python3
from pycnic.core import WSGI, Handler
import datetime
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

class Hello(Handler):

    def get(self, name="World"):
        return { 
            "message": "Hello, {name}!".format(name=name),
            "date": datetime.datetime.now()
        }


class app(WSGI):
    debug = True
    json_cls = DateTimeEncoder
    routes = [
        ("/", Hello()),
        ("/([\w]+)", Hello())
    ]

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    try:
        print("Serving on 0.0.0.0:8080...")
        make_server('0.0.0.0', 8080, app).serve_forever()
    except KeyboardInterrupt:
        pass
    print("Done")

