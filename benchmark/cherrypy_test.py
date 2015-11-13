import cherrypy
import json

class Root(object):
    
    @cherrypy.expose
    def json(self):
        return json.dumps({"message":"Hello, world!"})

app = cherrypy.tree.mount(Root())
cherrypy.log.screen = False
