#!/usr/bin/env python3
from pycnic.core import WSGI, Handler

class CorsTest(Handler):

    def get(self):
        return { 
            "message": "Cross site works!",
            "origin": self.request.get_header("Origin")
        }

    def options(self):
        return {
            "GET": {
                "description": "Test cross site origin",
                "parameters": None
             }
        }


class app(WSGI):

    # This allows * on all Handlers
    headers = [("Access-Control-Allow-Origin", "*")]

    routes = [
        ("/", CorsTest()),
    ]

if __name__ == "__main__":

    from wsgiref.simple_server import make_server
    try:
        print("Serving on 0.0.0.0:8080...")
        make_server('0.0.0.0', 8080, app).serve_forever()
    except KeyboardInterrupt:
        pass
    print("Done")

