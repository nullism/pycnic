[[
title: CLI Route Introspection
tags: [cli, examples]
]]

# CLI Routes

## Purpose

The `pycnic routes` CLI tool can be used for route introspection for pycnic
applications. It lists all the routes that it can identify from the 
`pycnic.core.WSGI.routes` list, as well as the methods that they support, and
the fully qualified handler object names.

## Usage

`pycnic routes [-sort {alpha,class,method}] [--verbose] routes [path]`

    -sort {alpha,class,method}  Sorting method to use, if any.
                                Alpha sorts by route regex, alphanumerically.
                                Class sorts by handler object names, alphanu-
                                merically.
                                Method groups supported request methods to-
                                gether.

    --verbose, -v               Provides verbose output about routes by dis-
                                playing their handler's docstring, if it has
                                one.

    path                        Python module-like path to describe what class
                                to print the routes of. Formatted as
                                path.to.file:class. For example, api.main:app
                                will access the app class in ./api/main.py.
                                Defaults to main:app.

## Example

    pycnic@pycnic:~/git/my_app $ ls
    LICENSE.md  README.md  main.py  routes.py  util.py
    pycnic@pycnic:~/git/my_app $
    pycnic@pycnic:~/git/my_app $ pycnic routes main:app
    Route    Method  Class

    /        GET     main.Index
    /ping    GET     main.Ping
    /login   POST    routes.Login
    /logout  POST    routes.Logout
    pycnic@pycnic:~/git/my_app $
    pycnic@pycnic:~/git/my_app $ pycnic routes -sort method main:app
    Method  Route    Class
    
    GET     /        main.Index
    GET     /ping    main.Ping
    
    POST    /login    routes.Login
    POST    /logout   routes.Logout
    pycnic@pycnic:~/git/my_app $

## Requirements

In order for route introspection to work, the application class being inspected
must be a subclass of `pycnic.core.WSGI`.