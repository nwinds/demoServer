import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.wsgi


import base64
import binascii
from hashlib import sha256
import hmac

import urllib
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
        """ interface for mod_a3e
            HTTP/1.1 302 Found
            Location: http://authServer/login?cid=xxxx&eid=xxxxx&url=xxxx
            url: urlencode+base6 https://gateway/index.php => aHR0cHM6Ly9nYXRld2F5L2luZGV4LnBocA%3D%3D
            cid: i.e: ClientID00000001
            eid: urlencode(base64(aes256_ecb(AuthKey, nonce | SSL Session ID | SSL Session LifeTime | AuthClientID)))
            currently: entire message without decoded, parse from passed in url
       """
        # original code
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

class GatewayHandler(tornado.web.RequestHandler):
    """
        HTTP/1.1 302 Found
        Location: https://gateway/index.php?tid=xxxx
        url(https://gateway/index.php)
        tid: urlencode(base64(sha256_hmac(authKey, cid | nonce))
        )
    """
    def get(self):
        self.write('<html><body><form action="/gateway" method="post">'
                   '<p>path: <input type="text" name="path"></p>'
                   '<p>cid: <input type="text" name="cid"></p>'
                   '<p>authKey: <input type="text" name="authKey"></p>'
                   '<p>nonce: <input type="text" name="nonce"></p>'
                   '<p><input type="submit" value="submit"></p>'
                   '</form></body></html>')

    def post(self):
        path = self.get_argument('path')
        cid = self.get_argument('cid')
        nonce = binascii.a2b_hex(self.get_argument('nonce'))
        authKey = self.get_argument('authKey')
        message = bytes(cid + nonce).encode('utf-8')
        secret = bytes(authKey).encode('utf-8')
        tid = hmac.new(secret, message, digestmod=sha256).digest()
        base64_tid = base64.b64encode(tid)
        another_sign = base64.b64encode(base64_tid)
        parses = {'tid': another_sign }
        url = '%s?%s' % (path, urllib.urlencode(parses))
        self.redirect(url)

class ParsegwHandler(tornado.web.RequestHandler):
    """ Parse request from gateway """

if __name__ == '__main__':
    tornado.options.parse_command_line()

    settings = {
            "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            "login_url": "/login",
            # "xsrf_cookies": True, # we ignore it now to test the correctness of redirect
    }

    """ /gateway : authServer redirect to gateway, passing url and tid as args(I remain empty interface currently) """
    app = tornado.web.Application(
        handlers=[(r'/', MainHandler),
                  (r'/login', LoginHandler),
                  (r'/poem', FormPageHandler),
                  (r'/gateway', GatewayHandler),
                  # (r"/gateway", tornado.web.RedirectHandler,
                    # dict(url="https://gateway/index.php")),
                  ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


