[[
title: Example validation
timestamp: 2015-10-03 23:02
tags: [examples]
]]

# Example Validation

## Using before 

The traditional way to handle validation is implementing
a `before` method on the handler.

    :::python
    from pycnic.core import Handler, WSGI
    from pycnic.errors import HTTP_400

    class NameHandler(Handler):
        
        def before(self):
            if 'name' not in self.request.data \
                    or self.request.data['name'] != 'root':
                raise HTTP_400("Expected 'root' as name")

        def post(self):
            return {"status": "ok"}

    class app(WSGI):
        routes = [('/name', NameHandler())]


## Using requires_validation decorator

As of `Pycnic v0.1.0` a Validation decorator is included
that accepts a validator function and re-raises an `HTTP_400`
error is that function raises any errors. 


    :::python
    from pycnic.core import Handler, WSGI
    from pycnic.utils import requires_validation
    
       
    def has_proper_name(data):
        if 'name' not in data or data['name'] != 'root':
            raise ValueError('Expected \'root\' as name')


    class NameHandler(Handler):

        @requires_validation(has_proper_name)
        def post(self):
            return {'status': 'ok'}


    class app(WSGI):
        routes = [('/name', NameHandler())]

