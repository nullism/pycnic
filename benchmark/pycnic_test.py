import sys;sys.path.insert(0,'../')

# TEST

#from pycnic.core import WSGI, Handler
import pycnic.core

class JSONHandler(pycnic.core.Handler):

    def get(self):
        return { "message": "Hello, World!" } 


class app(pycnic.core.WSGI):
    routes = [
        ("/json", JSONHandler()),
    ]

