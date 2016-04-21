import textwrap
import tornado.httpserver

import tornado.ioloop
import tornado.options
import tornado.web
# import tornado.wsgi
from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')
    # def post(self, widget_id):
        # widget = retrieve_from_db(widget_id)
        # widget['foo'] = self.get_argument('foo')
        # save_to_db(widget)


class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])

class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r"/", MainHandler),
                  (r"/reverse/(\w+)", ReverseHandler),
                  (r"/wrap", WrapHandler),
                  (r"/gateway", tornado.web.RedirectHandler,
                   dict(url="https://gateway/index.php")),
                  ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
