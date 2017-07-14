[[
title: Response Class
tags: [classes]
]]

# Response Class

The Response class contains data to be sent back to the client.

    :::python
    # cookies: A dictionary of cookies to be sent to the client.
    cookies = {}

    # set_header: A method that sets headers
    # to be sent back to the client
    set_header(self, key, value)

    # set_cookie: A method that sets cookies
    # to be sent back to the client with
    # Set-Cookie
    set_cookie(self, key, value, expires='', path='/', domain='')

    # delete_cookie: A method that tells the client to 
    # overwrite a cookie with a "bad" value.
    delete_cookie(self, key)

    # status_code: The integer HTTP code to return to the client
    status_code = 200

    # status: A read only property that returns a string
    # of the current self.status_code
    status = "200 OK"

        
    

