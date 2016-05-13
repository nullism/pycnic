import json
import sys

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
