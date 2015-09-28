# coding=utf-8
# Created by Anton Dementev on 23.09.15 

from tornado.escape import json_encode
from tornado.web import RequestHandler, asynchronous, HTTPError, ErrorHandler
import logging
import settings
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from application import helpers
from application.db import models

logger = logging.getLogger(__name__)


class BaseHandler(RequestHandler):

    def data_received(self, chunk):
        pass

    def head(self, *args, **kwargs):
        self.finish()

    def get_current_user(self):
        if self.get_secure_cookie("user"):
            return unicode(self.get_secure_cookie("user").replace("\"", ""), 'unicode-escape')
        else:
            return None

    def get_user_object(self):
        if self.get_secure_cookie("user"):
            try:
                return models.User.get(models.User.login == self.get_current_user())
            except models.User.DoesNotExist:
                return None
        else:
            return None

    def user_is_admin(self):
        user = self.get_user_object()
        return user and user.is_admin


class ErrorHandler(ErrorHandler, BaseHandler):

    def write_error(self, *args, **kwargs):
        page = settings.DOMAIN + self.request.uri
        self.render('404.html', page=page)


class LoginHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    def post(self, *args, **kwargs):
        login = self.get_body_argument("login", default=u"")
        password = self.get_body_argument("password", default=u"")
        next_page = self.get_body_argument("next", default=u"")
        error = u""
        if login == u"":
            error += u"Отсутствует логин."
        if password == u"":
            if len(error):
                error += u" "
            error += u"Отсутствует пароль."
        if len(error):
            self.render(
                "login.html",
                next=next_page,
                error=error,
                login=login,
                password=password
            )
        try:
            user = helpers.user_exist(login, password)
            self.set_secure_cookie("user", json_encode(user.login), expires_days=90)
            if next_page == u"" and user.is_admin:
                self.redirect(settings.ADMIN_REDIRECT)
            elif next_page == u"" and not user.is_admin:
                self.redirect(settings.CLIENT_REDIRECT)
            else:
                self.redirect(next_page)
        except helpers.AuthError as e:
            self.render(
                "login.html",
                next=next_page,
                error=e.message,
                login=login,
                password=password
            )

    def get(self, *args, **kwargs):
        next_page = self.get_query_argument("next", default="")
        self.render(
            "login.html",
            next=next_page,
            error=None,
            login=None,
            password=None
        )


class LogoutHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        admin = self.user_is_admin()
        self.clear_cookie("user")
        if admin:
            self.redirect("/login/?next=/")
        else:
            self.redirect("/login/?next=/")


class IndexHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        if not self.get_current_user():
            self.redirect("/login/?next=/")
        else:
            self.render("index.html")


class GetObjectHandler(BaseHandler):

    def data_received(self, chunk):
        pass

    def post(self, *args, **kwargs):
        if not self.user_is_admin():
            raise HTTPError(405)
        else:
            object_type = self.get_body_argument("object_type", default=u"")
            object_id = self.get_body_argument("object_id", default=0)
            if object_type == "":
                self.write({"result": False, "reason": u"Не указан тип объекта"})
            elif object_id == "" or int(object_id) == 0:
                self.write({"result": False, "reason": u"Не указан id объекта"})
            else:
                if object_type not in models.OBJECTS_TYPES.keys():
                    self.write({"result": False, "reason": u"Не найден тип объекта: {}".format(object_type)})
                else:
                    try:
                        obj = models.OBJECTS_TYPES[object_type].get(
                            models.OBJECTS_TYPES[object_type].id == int(object_id)
                        )
                        self.write({"result": True, "data": obj.get_dict()})
                    except models.OBJECTS_TYPES[object_type].DoesNotExist:
                        self.write(
                            {
                                "result": False,
                                "reason": u"Объект типа: '{0}' с id={1} в БД не найден".format(object_type, object_id)
                            }
                        )
