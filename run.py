import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.wsgi

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class FormPageHandler(tornado.web.RequestHandler):
    def post(self):
        # url = self.get_argument('url')
        # noun2 = self.get_argument('noun2')
        # verb = self.get_argument('verb')
        # noun3 = self.get_argument('noun3')
        self.redirect('gateway', permanent=True)# TODO handle url
        # self.render('form.html', roads=gwurl, wood=noun2, made=verb,
                # difference=noun3)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    # wsgi.WSGIApplication
    app = tornado.wsgi.WSGIApplication(
        handlers=[(r'/', IndexHandler), (r'/poem', FormPageHandler),
(r"/gateway", tornado.web.RedirectHandler,
                   dict(url="https://gateway/index.php")),


                  ],
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
