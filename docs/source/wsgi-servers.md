[[
title: WSGI Server Examples
description: Webservers and running Pycnic
timestamp: 2017-07-14 05:22
]]

[TOC]

# WSGI Server Examples

Here's a collection of examples using various WSGI servers to run a Pycnic app.

These examples assume you have an application in `hello.py` with a main WSGI class called `app`. 

    :::python
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

## [Gunicorn](http://gunicorn.org)

### Install

    :::text
    pip install gunicorn

### Run

    :::text
    gunicorn -b 0.0.0.0:8080 hello:app

## [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html)


### Install

    :::text
    pip install uwsgi

### Run

    :::text
    uwsgi --http 0.0.0.0:8080 --module hello:app

## [wsgiref](https://docs.python.org/2/library/wsgiref.html)

### Install

    :::text
    pip install wsgiref

### Run

First, in `hello.py` add

    :::python
    if __name__ == "__main__":
        from wsgiref.simple_server import make_server
        print("Serving on 0.0.0.0:8080...")
        make_server('0.0.0.0', 8080, app).serve_forever()

Then execute that script

    :::text
    python ./hello.py




