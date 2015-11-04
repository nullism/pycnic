import bottle

app = bottle.Bottle()

@app.route('/json')
def json():
    return {"message":"Hello, world!"}
