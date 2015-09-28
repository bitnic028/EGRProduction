# coding=utf-8
# Created by Anton Dementev on 23.09.15 

import handlers

urls = (
    (r"/", handlers.IndexHandler),
    (r"/login/", handlers.LoginHandler),
    (r"/logout/", handlers.LogoutHandler),
    (r"/get_object/", handlers.GetObjectHandler),
)
