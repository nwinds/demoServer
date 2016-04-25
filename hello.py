import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.wsgi


import base64
import binascii
import hash_sha256

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
        # cid = PARSE_ARGS_1
        # eid = PARSE_ARGS_2
        # url = PARSE_ARGS_3




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
# tornado.web.RedirectHandler
class GatewayHandler():
    """
    HTTP/1.1 302 Found
        Location: https://gateway/index.php?tid=xxxx
        url(https://gateway/index.php)
        tid: urlencode(base64(sha256_hmac(authKey, cid | nonce))
        )
    """
    def someMethod(self):
        """
        nonce: hard coded nonce
        """
        h_authKey_s = binascii.hexlify('ClientAuthKey001ClientAuthKey001')
        h_cid_s = binascii.hexlify('ClientID00000001')
        h_nonce_s = '0101010101010101'
        h_tid_s = hash_sha256.hmac(h_authKey_s, h_cid_s + h_nonce_s)


        # url = CONCATED_URL
        # tid = URL_ENCODED_TID
        base64_tid_encoded = base64.encodestring(h_tid_s)
        print(base64_tid_encoded)
        tid = urllib.urlencode(base64_tid_encoded)

        url = 'https://gateway/index.php'
        f = urllib.urlopen('%s?%s' % (url, tid))
        print(f.read())
        return (h_authKey_s, h_cid_s, h_nonce_s, h_tid_s, tid)




if __name__ == '__main__':
    tornado.options.parse_command_line()

    settings = {
            "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            "login_url": "/login",
            "xsrf_cookies": True,
    }

    """ /gateway : authServer redirect to gateway, passing url and tid as args(I remain empty interface currently) """
    app = tornado.wsgi.WSGIApplication(
        handlers=[(r'/', MainHandler),
                  (r'/login', LoginHandler),
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


