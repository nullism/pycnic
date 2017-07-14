[[
title: Example request data
timestamp: 2015-10-03 23:02
tags: [examples]
]]

# Example of the request object

The requests instance of the Request class contains information about... requests.

    :::python
    from pycnic.core import Handler, WSGI
    from pycnic.errors import HTTP_400

    class UsersHandler(Handler):

        def post(self):
             
            if not self.request.data.get("username"):
                raise HTTP_400("Yo dawg, you need to provide a username")

            return { 
                "username":self.request.data["username"],
                "authID":self.request.cookies.get("auth_id"),
                "yourIp":self.request.ip,
                "rawBody":self.request.body,
                "method":self.request.method,
                "json":self.request.data,
                "args":self.request.args,
                "jsonArgs":self.request.json_args,
                # Alternatively, self.request.environ.get("HTTP_X_FORWARDED_FOR")
                "xForwardedFor":self.request.get_header("X-Forwarded-For")
            }

    class app(WSGI):
        routes = [ ("/user", UserHandler()) ]

In the above example, several request properties are accessed. 

1. `self.request.method` - One of GET, POST, PUT, DELETE, OPTIONS.
2. `self.request.data` - When this property is read, it attempts to read the request body into a Python dictionary by way of JSON.
    If a body exists and it can't be read as JSON, then this sends an HTTP 400 JSON error to the client. 
3. `self.request.cookies` - A dictionary of client cookies available for this domain. 
4. `self.request.ip` - The IP address of the user. Pycnic attempts to use HTTP_X_FORWARDED_FOR if it's available, otherwise it settles 
    on REMOTE_ADDR.
5. `self.request.body` - This is the raw deal. The body contains everything that's not a header, read from wsgi.input. 
    This assumes CONTENT_LENGTH header was set. 
6. `self.request.args` - This is a dictionary of query string parameters. 
7. `self.request.json_args` - This is a dictionary of a loaded json string from the query parameters. 
    For example, a request to `/myurl?json=%7B%22foo%22%3A%22bar%22%7D` would populate `json_args` with `{"foo": "bar"}`. 
