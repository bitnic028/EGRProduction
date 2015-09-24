# coding=utf-8
# Created by Anton Dementev on 23.09.15 

import tornado.web
import tornado.httpserver
import tornado.ioloop
import logging.config
import urls
import handlers
import os
import sys
import inspect
from tornado.options import define, options
from settings import APP_SETTINGS, LOGGING

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

define("port", default=8888, help="run on the given port", type=int)
logging.config.dictConfig(LOGGING)
APP_SETTINGS["default_handler_class"] = handlers.ErrorHandler


class Application(tornado.web.Application):

    def __init__(self):
        settings = APP_SETTINGS
        tornado.web.Application.__init__(self, urls.urls, debug=True, **settings)


def main():
    options.parse_command_line()
    app = Application()
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.bind(options.port)
    server.start()
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()