import numpy as np

class Message(object):
    def __init__(self, msg_file="message.txt"):
        self.author = ""
        self.message = ""
        self.pathname = msg_file

    def __repr__(self):
        return "{} : {}".format(self.author, self.message)

    def save_txt(self):
        with open(self.pathname, "a", encoding="utf-8") as f:
            f.write(self.author + " : " + self.message + "<br>")
    
    def load_txt(self):
        with open(self.pathname, "r", encoding="utf-8") as f:
            return f.read()

def save_dict(pathname, dict):
    np.save(pathname, dict)

def load_dict(pathname):
    return np.load(pathname, allow_pickle=True).item()

def template(filename):
    with open("templates/" + filename, "r", encoding="utf-8") as f:
        return f.read()

def log(*args, **kwargs):
    print(*args, **kwargs)