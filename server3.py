#!/usr/bin/env python

# Uses redis + motor

import os.path # for template and static files
from bson.objectid import ObjectId
import json

# bunch of Tornado imports
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.options import define, options


import tornadoredis
from motor import MotorClient

import settings
from settings import MONGO_URL

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/(\w+)', MainHandler)
        ]
        app_settings = settings.application_handler_setttings
        conn = MotorClient(MONGO_URL)
        self.db = conn["tornado_bench"]
        tornado.web.Application.__init__(self, handlers, **app_settings)


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, post_id):

        c = tornadoredis.Client()

        blog_post = yield gen.Task(c.get, post_id)

        if blog_post:
            blog_post = json.loads(blog_post)
        else:
            blog_db = self.application.db.blog
            blog_post = yield blog_db.find_one({'_id': ObjectId(post_id)})
            with c.pipeline() as pipe:
                blog_post['_id'] = ""
                pipe.set(post_id, json.dumps(blog_post))
                yield gen.Task(pipe.execute)

        self.render('index.html', blog_post=blog_post)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
