import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.wsgi


import os

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # tornado.web.authenticated did the following work
        # secure cookie - ver 1.0
        # if not self.current_user:
            # self.redirect("/login")
            # return

        # if not self.get_secure_cookie("mycookie"):
            # self.set_secure_cookie("mycookie", "myvalue")
            # self.write("Your cookie was not set yet!")
        # else:
        name  = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("template.html", title="My title", items=items)
        self.render('index.html')

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="login" method="post">'
                   'Name: <input type="text" name="name">'
                   ' <input type="submit" value="Sign in">'
                   ' </form></body></html>')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

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

    settings = {
            "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            "login_url": "/login",

    }

    app = tornado.wsgi.WSGIApplication(
        handlers=[(r'/', MainHandler),
                  (r'login', LoginHandler),
                  (r'/poem', FormPageHandler),
                  (r"/gateway", tornado.web.RedirectHandler,
                    dict(url="https://gateway/index.php")),
                  ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


