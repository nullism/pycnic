#!/usr/bin/env python3
import re
import traceback
import json
import logging

from .data import STATUSES
from . import errors


class Request(object):

    _body = None
    _data = None

    def __init__(self, path, method, environ):
        self.path = path
        self.method = method.upper()
        self.environ = environ
        
    @property
    def body(self):
        if self._body:
            return self._body
        try:
            length = int(self.environ.get("CONTENT_LENGTH", "0"))
        except ValueError:
            length = 0
        if length > 0:
            self._body = self.environ['wsgi.input'].read(length)

        return self._body

    @property
    def data(self):
        if self._data:
            return self._data
        if self.body:
            self._data = json.loads(self.body.decode('utf-8'))
            return self._data
        return None

    @property
    def ip(self):
        try:
            return self.environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
        except KeyError:
            return self.environ['REMOTE_ADDR']

class Response(object):
    
    header_dict = { 
        "Content-Type": "application/json"
    }

    _headers = []

    def __init__(self, status_code):
        self.status_code = status_code

    def set_header(self, key, value):
        self.header_dict[key] = value
        
    @property
    def headers(self):
        self._headers = []
        for k,v in self.header_dict.items():
            self._headers.append((k, v))
        return self._headers

    @property
    def status(self):
        if self.status_code in STATUSES:
            return STATUSES[self.status_code]
        return STATUSES[577]

class WSGI:

    routes = []
    debug = False
    logger = None
    before = None
    after = None
        
    def __init__(self, environ, start_response):
        if not self.logger:
            self.logger = logging.Logger(__name__)
        self.logger.info("__init__ called")

        self.request = Request(
            path=environ["PATH_INFO"],
            method=environ["REQUEST_METHOD"],
            environ=environ
        )

        self.response = Response(
            status_code = 200
        )

        self.environ = environ
        self.start = start_response
                
        self.response.set_header("Content-Type", "application/json")
       
            
    def __iter__(self):
        try:
            if self.before:
                self.before()
            resp = self.delegate()
            if self.after:
                self.after()
            self.start(self.response.status, self.response.headers)

        except errors.HTTPError as err:
            self.response.status_code = err.status_code
            headers = [("Content-Type", "application/json")]
            self.start(self.response.status, headers)
            resp = err.response()
    
        except Exception as err:
            self.logger.exception(err)
            headers = [("Content-Type", "application/json")]
            self.start(STATUSES[500], headers)
            if self.debug:
                resp = { "error": traceback.format_exc()}
            else:
                resp = { "error": "Internal server error encountered." }
            
        # return value can be a string or a list. we should be able to 
        # return an iter in both the cases.
        if isinstance(resp, dict):
            return iter([json.dumps(resp).encode('utf-8')])
        elif isinstance(resp, str):
            return iter([resp.encode('utf-8')])
        else:
            return iter(resp)

    def delegate(self):
        path = self.request.path
        method = self.request.method
                
        for pattern, handler in self.routes:
            # Set defaults for handler
            handler.request = self.request
            handler.response = self.response
            
            if hasattr(handler, 'before'):
                handler.before()

            m = re.match('^' + pattern + '$', path)
            if m:
                args = m.groups()
                funcname = method.lower()
                try:
                    func = getattr(handler, funcname)
                except AttributeError:
                    raise errors.HTTP_405("%s not allowed"%(method.upper()))

                output = func(*args)

                if hasattr(handler, 'after'):
                    handler.after()

                return output
                               
        raise errors.HTTP_404("Path %s not found"%(path))

class Handler(object):
    request = None
    response = None 


