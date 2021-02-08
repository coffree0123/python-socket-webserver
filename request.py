import urllib.parse

from cookie import add_cookie, add_account, delete_cookie, check_cookie, check_account, check_account_exist
from toolbox import Message, save_dict, load_dict, template, log

class Request(object):
    def __init__(self):
        self.path = ""
        self.query = {}
        self.method = "GET"
        self.body = ""

    def parse_path(self, path):
        idx = path.find("?")
        query = {}
        if idx != -1:
            path, query_s = path.split("?", 1)
            args = query_s.split('&')
            # message=1 -> message:1 for all &
            for arg in args:
                key, value = arg.split("=")
                query[key] = value
        self.path = path
        self.query = query

    def parse_body(self):
        # url ASCII code decode
        self.body = urllib.parse.unquote(self.body)
        log("body is ", self.body)
        args = self.body.split("&")
        f = {}
        for arg in args:
            key, value = arg.split("=")
            f[key] = value
        return f

    def get_cookie(self, receive_message):
        cookie_str = receive_message.split("\r\n")[-3]
        self.cookie = cookie_str.split("=")[1]
        log("Cookie:", self.cookie)

    def route_index(self):
        header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        body = template("index.html")
        reply = header + body
        return reply.encode(encoding="utf-8")

    def route_message(self):
        msgs = ""
        msg = Message()
        if self.method == "POST":
            # Parse body.
            body = self.parse_body()
            msg.author = body.get("author", "")
            msg.message = body.get("message", "")
            msg.save_txt()
        
        # Load previous message from file.
        try:
            msgs = msg.load_txt()
        except:
            pass
        header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        body = template("message.html")

        log("msgs ", msgs)
        
        body = body.replace('{{message}}', msgs)
        reply = header + body
        return reply.encode(encoding="utf-8")

    def route_account(self):
        create_success = False
        if self.method == "POST":
            # Parse body.
            body = self.parse_body()
            username = body.get("username", "")
            password = body.get("password", "")
            # Check if this username is used.
            if not (check_account_exist(username, password)) and (username != ""):
                add_account(username, password)
                # Add this user to account_list.
                log("username and password", username, password)
                create_success = True

        header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        body = template("create_success.html") if create_success else template("account.html")

        if not create_success:
            # Decide if user create account or not.
            if (self.method == "POST"):
                body = body.replace('{{message}}', "This username cannot be used !")
            else:
                body = body.replace('{{message}}', "")

        reply = header + body
        return reply.encode(encoding="utf-8")

    def route_login(self):
        # Check if user logged in before.
        if (check_cookie(self.cookie)):
            header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            body = template("login_success.html")
            reply = header + body
            return reply.encode(encoding="utf-8") 

        login_success = False
        # If body is empty means that it is jump from somewhere.
        if self.method == "POST":
            # Parse body.
            body = self.parse_body()
            username = body.get("username", "")
            password = body.get("password", "")
            # Add this user to account_list.
            login_success = check_account(username, password)

        header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        body = template("login_success.html") if login_success else template("login.html")
        if not login_success:
            # Decide if user enter account or not.
            if (self.method == "POST"):
                body = body.replace('{{message}}', "Wrong username or password !")
            else:
                body = body.replace('{{message}}', "")
        else:
            add_cookie(self.cookie, username)

        reply = header + body
        return reply.encode(encoding="utf-8")

    def route_starburst(self):
        if not (check_cookie(self.cookie)):
            header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            body = template("login.html")
            body = body.replace('{{message}}', "")
            reply = header + body
            return reply.encode(encoding="utf-8")

        header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        body = template("starburst.html")

        reply = header + body
        return reply.encode(encoding="utf-8")


    def route_logout(self):
        delete_cookie(self.cookie)
        header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        body = template("logout.html")
        reply = header + body
        return reply.encode(encoding="utf-8")

    def route_login_img(self):
        with open("./img/kirito.gif", "rb") as f:
            header = b"HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n"
            img = header + f.read()
            return img

    def route_logout_img(self):
        with open("./img/game_over.jpg", "rb") as f:
            header = b"HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n"
            img = header + f.read()
            return img

    def route_boss_img(self):
        with open("./img/boss.jpg", "rb") as f:
            header = b"HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n"
            img = header + f.read()
            return img

    def route_starburst_img(self):
        with open("./img/fail.gif", "rb") as f:
            header = b"HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n"
            img = header + f.read()
            return img

    def error(self, code=404):
        err_dict = {
            404: b'HTTP/1.1 404 NOT FOUND\r\n<h1>404 NOT FOUND</h1>',
            405: b'',
        }
        return err_dict.get(code, b'')

    def response(self):
        reply = {
            '/': self.route_index,
            '/login': self.route_login,
            '/logout': self.route_logout,
            '/message': self.route_message,
            '/starburst': self.route_starburst,
            '/img/login': self.route_login_img,
            '/img/logout': self.route_logout_img,
            '/img/boss': self.route_boss_img,
            '/img/starburst': self.route_starburst_img,
            '/create_account': self.route_account
        }

        # Return route function
        response_f = reply.get(self.path, self.error)
        return response_f()