import cherrypy

class Root(object):
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def json(self):
        return {"message":"Hello, world!"}

app = cherrypy.tree.mount(Root())
cherrypy.log.screen = False
