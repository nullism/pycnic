import muffin

app = muffin.Application('web')

@app.register('/json')
def json(request):
    return { 'message': 'Hello, World!' }

