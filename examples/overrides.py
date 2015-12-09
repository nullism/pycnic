#!/usr/bin/env python3
from pycnic.core import WSGI, Handler
import logging
import sys

my_logger = logging.Logger(__name__)
my_logger.setLevel(logging.DEBUG)
hnd = logging.StreamHandler(sys.stdout)
my_logger.addHandler(hnd)

"""
overrides.py

This example includes special methods, functions, and properties
with example usages.
"""

def my_before(handler):
    
    my_logger.info("Before, request IP is %s"%(handler.request.ip))

def my_after(handler):

    my_logger.info("After, headers are %s"%(handler.response.headers))

class Howdy(Handler):

    def before(self):
        """ Called before the request is routed """

        my_logger.info("Howdy before called") 

    def after(self):
        """ Called after the request is routed """

        my_logger.info("Howdy after called")
    
    def get(self):

        assert self.request.method == "GET"
        return {}

    def post(self):
        
        assert self.request.method == "POST"
        return {}

    def put(self):

        assert self.request.method == "PUT"
        return {}

    def delete(self):

        assert self.request.method == "DELETE"
        return {}

class app(WSGI):

    # A method name to call before the request is routed
    # default: None
    before = my_before

    # A method name to call after the request is routed
    # default: None
    after = my_after

    # Assign a custom logger, default is logging.Logger
    logger = my_logger

    # Set debug mode, default False
    debug = True

    # Remove the trailing slash for routing purposes
    # default: True
    strip_path = True

    # A list of routes, handler instances
    routes = [
        ('/', Howdy()),
    ]
    
if __name__ == "__main__":

    from wsgiref.simple_server import make_server
    try:
        print("Serving on 0.0.0.0:8080...")
        make_server('0.0.0.0', 8080, app).serve_forever()
    except KeyboardInterrupt:
        pass
    print("Done")
 
