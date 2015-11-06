#!/usr/bin/env python3
from pycnic.core import WSGI, Handler
from pycnic.errors import HTTPError



def before(handler):
    if handler.request.ip in ['1.2.3.4', '5.6.7.8']:
        raise HTTPError(401, "Hey! You're banned from here.")        

class IndexHandler(Handler):

    def get(self, name="Nobody"):
        return { 
            "message":"How you is, %s?"%(name), 
            "path":self.request.path,
            "requestBody":self.request.body,
            "status":self.response.status,
            "clientIp":self.request.ip,
            "cookies":self.request.cookies,
        }

    def post(self):
        data = self.request.data
        self.response.status_code = 201
        return { 
            "message":"thanks for the datas"
        }    

class application(WSGI):
    routes = [
        ("/", IndexHandler()),
        ("/name/(.*)", IndexHandler())
    ]
    debug = True
    before = before

if __name__ == "__main__":

    from wsgiref.simple_server import make_server
    try:
        print("Serving on 0.0.0.0:8080...")
        make_server('0.0.0.0', 8080, application).serve_forever()
    except KeyboardInterrupt:
        pass
    print("Done")

