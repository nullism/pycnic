[[
title: Example Error Handling
timestamp: 2015-11-05 22:21
tags: [examples]
]]

# Example error handling

`pycnic.errors` provides several exception classes. 

* HTTPError - The parent error.
* HTTP_400/401/403/404/405 - For 4xx client errors.
* HTTP_500 - For 5xx server errors.

The Pycnic framework catches these built-in exceptions and returns json describing the error (defined in the exception's `response` method). 
The `response` method returns a dictionary which is then encoded into JSON and sent back to the client.

By default, any HTTPError subclass sends the following response to the client when the exception is caught:

    :::python
    {
        "status": self.status,
        "status_code": self.status_code,
        "error":self.message,
        "data":self.data
    }

* `status` is a string like "404 Not Found".
* `status_code` is the integer representation, like 404.
* `error` is the error message from the exception.
* `data` is a custom attribute that defaults to null.

## Using Exceptions

Exceptions are wonderful and easy to use.
Let's say you have a Handler that requires a message from the user on POST. 
If that message isn't present, you could manually set the status and 
return your own message, or you could do something like below: 

    :::python
    class MessageHandler(Handler):
        def post(self):
            if not self.request.data.get("message"):
                raise HTTP_400("Message is required")
            return { 
                "youSaid":self.request.data["message"]
            }

## Custom Exceptions

Pycnic makes it easy to write and use your own exceptions.
 
Let's say your application checks for authorization frequently. 
Instead of doing `raise HTTP_401("You can't do that, please login", data={"loginURI":"/login"})` each 
time a user isn't authorized, you can create your own exception class.

    :::python
    class AuthError(pycnic.errors.HTTPError):

        status_code = 401 # Required
        message = "You can't do that, please login"

        def __init__(self):
            pass

        def response(self):
            return { 
                "error":self.message,
                "data": { "loginURI":"/login" },
                "status_code":self.status_code,
                "status":"401 Not Authorized"
            }

You can then raise that exception when appropriate.

    :::python
    class SomeHandler(Handler):
        def get(self):
            if not logged_in(self.request):
                raise AuthError()
            ...


Which, if the user is not logged in, will return a 401 response with a JSON body of: 

    :::json
    {
        "data": {"loginURI": "/login"}, 
        "status": "401 Not Authorized", 
        "error": "You can't do that, please login", 
        "status_code": 401
    }
