[[
title: Introduction
description: Pycnic, the JSON API framework
timestamp: 2015-10-01 20:22
]]

# What it be? 

Pycnic is a small, fast, easy to use web framework for building JSON APIs. 

# What it do? 

Pycnic handles routing, JSON requests and responses, cookie magic, and provides 
jsonified error handling. 

# Get it

GitHub: [github.com/nullism/pycnic](https://github.com/nullism/pycnic)

PyPI: [pypy.python.org/pypi/pycnic](https://pypi.python.org/pypi/pycnic)

Or with pip: `pip install pycnic`

# Quick sample

    :::python
    # from hello.py
    from pycnic.core import WSGI, Handler

    class Hello(Handler):

        def get(self, name="World"):
            return {
                "message": "Hello, {name}!".format(name=name)
            }


    class app(WSGI):
        routes = [
            ("/", Hello()),
            ("/([\w]+)", Hello())
        ]


To run the example, just point some WSGI server at it, like [Gunicorn](http://gunicorn.org).

    :::bash
    gunicorn hello:app

