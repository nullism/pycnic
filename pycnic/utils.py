import json
import sys
from functools import wraps

from . import errors

if sys.version_info >= (3, 0):
    from urllib.parse import parse_qsl
else:
    from cgi import parse_qsl

def query_string_to_dict(qs):
    """ Returns a dictionary from a QUERY_STRING """

    pairs = parse_qsl(qs)
    if pairs:
        return dict(pairs)
    return {}

def query_string_to_json(qs):
    """ Returns a dictionary from a QUERY_STRING with JSON in it """

    if "json=" not in qs:
        return {}
    data = query_string_to_dict(qs)
    return json.loads(data.get("json","{}"))


def requires_validation(validator, with_route_params=False):
    """ Validates an incoming request over given validator. 
    If with_route_params is set to True, validator is called with request
    data and args taken from route, otherwise only request data is
    passed to validator. If validator raises any Exception, HTTP_400 is raised.
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                if with_route_params:
                    validator(args[0].request.data, args[1:])
                else:
                    validator(args[0].request.data)
            except Exception as e:
                raise errors.HTTP_400(str(e))

            return f(*args, **kwargs)
        return wrapped
    return wrapper
