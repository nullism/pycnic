#!/usr/bin/env python3
import tornado.ioloop
import tornado.web

class JSONHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({"message":"Hello, world!"})

app = tornado.web.Application([
    (r"/json", JSONHandler),
])

if __name__ == "__main__":
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
