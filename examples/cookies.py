#!/usr/bin/env python3
import sys; sys.path.insert(0, '../')
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

if __name__ == "__main__":

    from wsgiref.simple_server import make_server
    try:
        print("Serving on 0.0.0.0:8080...")
        make_server('0.0.0.0', 8080, app).serve_forever()
    except KeyboardInterrupt:
        pass
    print("Done")

