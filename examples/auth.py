#!/usr/bin/env python3
from functools import wraps
from pycnic.core import WSGI, Handler
from pycnic.errors import HTTP_401

def get_user_role(request):
    # Normally you'd do something like 
    # check for request.cookies["session_id"]
    # existing in memcache or a database, but
    # for now... everyone's an admin!
    return "admin"

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_user_role(args[0].request) not in roles:
                raise HTTP_401("I can't let you do that")
            return f(*args, **kwargs)
        return wrapped
    return wrapper

class UserHandler(Handler):
    
    @requires_roles("admin", "user")
    def get(self):
        return { "message":"Welcome, admin!" }

    @requires_roles("admin")
    def post(self):
        self.response.status_code = 201
        return { "message":"New user added!" }

class app(WSGI):
    routes = [ ('/user', UserHandler()) ]

if __name__ == "__main__":

    from wsgiref.simple_server import make_server
    try:
        print("Serving on 0.0.0.0:8080...")
        make_server('0.0.0.0', 8080, app).serve_forever()
    except KeyboardInterrupt:
        pass
    print("Done")
