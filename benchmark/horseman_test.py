from horseman.response import Response
from roughrider.application import Application

app = Application()


@app.routes.register('/json')
def json(request):
    return Response.to_json(body={'message': "Hello, world!"})
