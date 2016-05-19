#!/usr/bin/env python3
import re
import traceback
import json
import logging

from . import utils
from .data import STATUSES
from . import errors


class Handler(object):

    request = None
    response = None 


class Request(object):

    def __init__(self, path, method, environ):
        self._headers = None
        self._args = None
        self._json_args = None
        self._cookies = None
        self._body = None
        self._data = None

        self.path = path
        self.method = method.upper()
        self.environ = environ
    
    def get_header(self, name, default=None):
        return self.headers.get(name.title(), default)

    @property
    def headers(self):
        if self._headers is not None:
            return self._headers
        self._headers = {}
        for key, value in self.environ.items():
            if key == "CONTENT_TYPE" or key == "CONTENT_LENGTH":
                header = key.title().replace("_", "-")
                self._headers[header] = value
            elif key.startswith("HTTP_"):
                header = key[5:].title().replace("_", "-")
                self._headers[header] = value
        return self._headers

    @property
    def args(self):
        if self._args is not None:
            return self._args
        qs = self.environ["QUERY_STRING"]
        self._args = utils.query_string_to_dict(qs)
        return self._args

    @property
    def json_args(self):
        if self._json_args is not None:
            return self._json_args

        try:
            qs = self.environ["QUERY_STRING"]
            self._json_args = utils.query_string_to_json(qs) 
        except Exception:
            raise errors.HTTP_400("Invalid JSON in request query string") 

        return self._json_args
 
    @property
    def body(self):
        if self._body is not None:
            return self._body
        try:
            length = int(self.environ.get("CONTENT_LENGTH", "0"))
        except ValueError:
            length = 0
        if length > 0:
            self._body = self.environ['wsgi.input'].read(length)
        else:
            self._body = ''

        return self._body

    @property
    def cookies(self):
        if self._cookies is not None:
            return self._cookies

        self._cookies = {}

        if 'HTTP_COOKIE' in self.environ:
            for cookie_line in self.environ['HTTP_COOKIE'].split(';'):
                if "DELETED" in cookie_line:
                    continue
                cname, cvalue = cookie_line.strip().split('=',1)
                self._cookies[cname] = cvalue

        return self._cookies

    @property
    def data(self):
        if self._data is not None:
            return self._data
        if self.body:
            try:
                self._data = json.loads(self.body.decode('utf-8'))
            except Exception:
                raise errors.HTTP_400("Expected JSON in request body")
        else:
            self._data = {}

        return self._data

    @property
    def ip(self):
        try:
            return self.environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
        except KeyError:
            return self.environ['REMOTE_ADDR']

class Response(object):
    

    def __init__(self, status_code):
        self.header_dict = { 
            "Content-Type": "application/json"
        }
        self._headers = []
        self.cookie_dict = {}
        self.status_code = status_code

    def set_header(self, key, value):
        self.header_dict[key] = value

    def set_cookie(self, key, value, expires="", path='/', domain=""):
        value = value.replace(";","") # ; not allowed
        if expires:
            expires = "expires=%s; "%(expires)
        if domain:
            domain = "Domain=%s; "%(domain)
        self.cookie_dict[key] = "%s;%s%s path=%s"%(value, domain, expires, path)
        
    def delete_cookie(self, key):
        self.set_cookie(key, "DELETED", expires="Thu, 01 Jan 1970 00:00:00 GMT")

    @property
    def headers(self):
        self._headers = []
        for k,v in self.header_dict.items():
            self._headers.append((k, v))
        for k,v in self.cookie_dict.items():
            self._headers.append(('Set-Cookie', '%s=%s'%(k,v)))
        return self._headers

    @property
    def status(self):
        if self.status_code in STATUSES:
            return STATUSES[self.status_code]
        print("Warning! Status %s does not exist!"%(self.status_code))
        return STATUSES[577]

class WSGI:

    routes = []
    debug = False
    logger = None
    before = None
    after = None
    strip_path = True
        
    def __init__(self, environ, start_response):

        if not self.logger:
            self.logger = logging.Logger(__name__)

        self.logger.info("__init__ called")

        path = environ["PATH_INFO"]
        if self.strip_path and len(path) > 1 and path.endswith("/"):
            path = path[0:-1]

        self.request = Request(
            path=path,
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
            if err.headers:
                headers += err.headers
            self.start(self.response.status, headers)
            resp = err.response()
    
        except Exception as err:
            self.logger.exception(err)
            headers = [("Content-Type", "application/json")]
            self.start(STATUSES[500], headers)
            if self.debug:
                resp = { "error": traceback.format_exc().split("\n")}
            else:
                resp = { "error": "Internal server error encountered." }
            
        if isinstance(resp, dict):
            if self.debug:
                jresp = json.dumps(resp, indent=4)
            else:
                jresp = json.dumps(resp)
            return iter([jresp.encode('utf-8')])
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

            m = re.match('^' + pattern + '$', path)
            if m:
                if hasattr(handler, 'before'):
                    handler.before()

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


