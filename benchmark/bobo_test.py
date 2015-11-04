import bobo

@bobo.query('/json', content_type='application/json')
def json():
    return { "message":"Hello, world!" }


