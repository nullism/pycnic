[[
title: Getting started
timestamp: 2015-10-03 22:19
]]

[TOC]

# Getting Started

## Install

The easiest way to install Pycnic is though `pip`. 

    pip install pycnic

Or, for Python 3:

    pip3 install pycnic

Now Pycnic is ready to be used.

## Making an App

Let's create a new file called `quote.py`

    :::python
    # quote.py
    from pycnic.core import WSGI, Handler

    class QuoteRes(Handler):
        def get(self):
            return { 
                "quote":"Cool URIs don't change",
                "author":"Tim Berners-Lee"
            }

    class app(WSGI):
        routes = [('/', QuoteRes())]

The basic structure of this app is as follows: 

1. The `QuoteRes` subclass of `Handler`. This exposes `get, post, put, delete`, and `options` methods 
of your subclass to the client if those methods are implemented. For now, we only care about `get`. 
2. The `app` subclass of `WSGI`. This is a wsgi class with some configuration options. 
For now, we only care about routing '/' to `QuoteRes`.  

## Running an App

Since Pycnic is WSGI compliant, running this app can be done a number of ways. 

For this example, let's use [Gunicorn](http://gunicorn.org).

### Installing Gunicorn

Gunicorn is available in the Python Package Index, so it can be installed with 

    pip install gunicorn

Or, for Python 3

    pip3 install gunicorn

### Hosting with Gunicorn

In the same directory as `quote.py`, run

    gunicorn quote:app

Your app should now be hosted.

    :::text
    [2015-11-03 13:03:09 -0500] [7292] [INFO] Starting gunicorn 19.3.0
    [2015-11-03 13:03:09 -0500] [7292] [INFO] Listening at: http://127.0.0.1:8000 (7292)
    ...

If you visit [http://localhost:8000/](http://localhost:8000/) you should see a response like the following:

    :::json
    {"quote": "Cool URIs don't change", "author": "Tim Berners-Lee"}
