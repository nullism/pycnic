import cherrypy
import json

class JSONRoot(object):
    
    @cherrypy.expose
    def index(self):
        return json.dumps({"message":"Hello, world!"})

app = cherrypy.tree.mount(JSONRoot(), "/json")
