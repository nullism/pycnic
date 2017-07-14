[[
title: WSGI Class
tags: [configuration, classes]
]]

# WSGI Class

## Configuration

The WSGI class contains several configuration properties for use in your `app` subclass.

    :::python
    class app(pycnic.core.WSGI):

        # logger: A Python logging Logger instance
        logger = logging.Logger(__name__)

        # before: A function that accepts a WSGI instance 
        # as its first argument. Executed before dispatching
        # the request. Does not need to return.
        before = None

        # after: A function that accepts a WSGI instance
        # as its first argument. Executed after dispatching 
        # the request if no errors are raised. Does not need to return.
        after = None

        # teardown: A function that accepts a WSGI instance
        # as its argument. Always executed at the end of the request
        # even if errors are raised.
        # New in v0.1.1
        teardown = None

        # headers: default headers to add to the response
        # on every successful request, or when an HTTP* error
        # is raised. In the format of [("key", "value"),("key", "value")]
        # New in v0.1.1
        headers = None

        # debug: Boolean. If true, will return error stacktraces
        # for uncaught exceptions and json will be pretty-formatted.
        debug = False

        # strip_path: Boolean. If true, paths with a trailing 
        # slash (/foo/bar/) will have the trailing slash removed 
        # (/foo/bar) before routing the request
        strip_path = True

        # routes: A list of (path, Handler()) tuples.
        routes = []


