import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.wsgi


import os

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # secure cookie - ver 1.0
        if not self.get_secure_cookie("mycookie"):
            self.set_secure_cookie("mycookie", "myvalue")
            self.write("Your cookie was not set yet!")
        else:
            self.write("Your cookie was set!")
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
        handlers=[(r'/', MainHandler),
                  (r'/poem', FormPageHandler),
                  (r"/gateway", tornado.web.RedirectHandler,
                    dict(url="https://gateway/index.php")),
                  ], cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


