import hug
import json


@hug.get('/json')
def json_get():
    return { "message": "Hello, World!" } 
