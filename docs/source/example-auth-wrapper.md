[[
title: Example Authentication Wrapper
timestamp: 2015-11-03 23:45
tags: [examples]
]]

# Example Authentication Wrapper

Handling authentication with a wrapper just *feels* clean. 

    :::python
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

As you can see from above, either a user or admin can perform a GET request 
against the `UserHandler`, but only an admin can POST to it. 

In that example, `get_user_role()` is a dummy function that blindly returns 
"admin" for each user. 


