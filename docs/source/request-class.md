[[
title: Request class
tags: [classes]
]]

# Request Class

The request instance provided in self.request contains the following properties.

    :::python
    # cookies: A dictionary of client cookies 
    # in the format of { cookie name: cookie value }
    cookies = {}

    # headers: A dictionary of title-case headers
    # in the format of { Header-Name: value }
    # Example: headers['Content-Length']
    headers = {}

    # get_header: A method to return a header in self.headers
    # or default if it is not set. 
    get_header(self, name, default=None)

    # method: The request method, upper case.
    # may be GET, POST, PUT, DELETE, OPTIONS
    method = None 

    # ip: The IP address of the client. If a X-Forwarded-For IP exists,
    # it will use that instead (for proxies)
    ip = None

    # body: The raw request body as read from wsgi.input
    # This relies on a content-length header being present.
    body = None

    # data: A dictionary built from JSON in the request body.
    # If the body does not contain valid json when this property
    # is accessed it will raise an HTTP_400 error.
    data = {}

    # args: A dictionary built from the query string parameters.
    args = {}

    # json_args: A dictionary built from "json=" in the query string.
    # If the query string does not contain "json=" then this will be {}.
    # If the query string contains "json=" but it is invalid JSON, then 
    # this will raise an HTTP_400 error.
    json_args = {}

    # environ: The WSGI environ dictionary
    environ = wsgi.environ


