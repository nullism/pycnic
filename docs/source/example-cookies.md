[[
title: Working with Cookies
timestamp: 2015-11-07 09:00
tags: [examples]
]]

# Working with Cookies

Cookies can be accessed in the `request` and `response` objects.

## Read

To read a cookie:

    :::python
    self.request.cookies # Dictionary of all client-cookies
    self.request.cookies.get("Cookie name") # get a specific cookie

## Set

Setting a cookie only requires a key and value for the cookie.

To set a cookie:

    :::python
    self.response.set_cookie(
        "Cookie name", 
        "Cookie Value", 
        expires="Optional time string, default: empty", 
        domain="Optional domain, default: empty",
        path="Optional path, default: /",
        flags=["List", "OfFlags", "default: []"])

*Note: `flags` is available as of v0.1.2*

If the expiration date is not specified then most browsers will
treat this as a Session cookie, which lasts until "removed" by the server.

## Delete

When a cookie is deleted, its value is replaced with **DELETED** and
the expiration is set to *Jan 1st, 1970*. Pycnic ignores cookies
that contain *DELETED* in the value. 

To delete a cookie:

    :::python
    self.response.delete_cookie("Cookie name")

## Full example

    :::python
    from pycnic.core import WSGI, Handler
    from pycnic.errors import HTTP_400, HTTP_401

    class Login(Handler):

        def get(self):

            sess_id = self.request.cookies.get("session_id")
            return { "session_id":sess_id }

        def post(self):

            username = self.request.data.get("username")
            password = self.request.data.get("password")

            if not username or not password:
                raise HTTP_400("Username and password are required")

            if username != "foo" or password != "foo":
                raise HTTP_401("Username or password are incorrect")

            # Set a session ID for lookup in a DB or memcache
            self.response.set_cookie("session_id", "1234567890abcdefg")
            return { "message":"Logged in" }

    class Logout(Handler):

        def post(self):

            if self.request.cookies.get("session_id"):
                # Clear the cookie
                self.response.delete_cookie("session_id")
                return { "message":"Logged out" }

            return {
                "message":"Already logged out",
                "cookies":self.request.cookies
            }

    class app(WSGI):
        routes = [
            ("/login", Login()),
            ("/logout", Logout()),
        ]

