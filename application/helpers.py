# coding=utf-8
# Created by Anton Dementev on 22.09.15 
from datetime import datetime
import hashlib
from server import settings
from db.models import User


class DateFormats:
    short = u"{0}-{1}-{2}"
    long = u"{0} {1} {2} г."


def string_from_date(date, format_type):
    """
    Convert date to different string presentations
    :param date: datetime.datetime
    :param format_type: string or unicode string. Possible values: "short1", "short2" and "long"
    :return: if date = 1.01.2015 "short1" -> "01-01-2015", "short2" -> "1-1-2015", "long" -> "10 января 2015 г."
    """
    if format_type == u"short1":
        return date.strftime("%d-%m-%Y")
    elif format_type == u"short2":
        return DateFormats.short.format(date.day, date.month, date.year)

    else:
        return DateFormats.long.format(date.day, settings.MONTHES_LONG[date.month - 1], date.year)


def rounded_date(date):
    """
    Round date to day without hours, minutes and seconds eg. 10.10.2010 00:00
    :param date: datetime.datetime
    :return: datetime.datetime with params: hours=0 minutes=0 seconds=0
    """
    return datetime.strptime(string_from_date(date, u"short2").encode("utf8"), "%d-%m-%Y")


class AuthError(Exception):
    pass


def create_hash(login, password):
    """
    Create and return hash from login & password
    :param login: string
    :param password: string
    :return: hash
    """
    s = login.encode("utf-8") + settings.HASH_SALT + password.encode("utf-8")
    return hashlib.sha256(s).hexdigest()


def user_exist(login, password):
    """
    Check if User exist in db. Raises AuthError exception if something goes wrong
    :param login: string
    :param password: string
    :return: User object
    :raise AuthError:
    """
    try:
        user = User.get(User.login == login)
    except User.DoesNotExist:
        raise AuthError(u"Пользователь с логином {} не найден в базе данных".format(login))
    if create_hash(login, password) == user.password:
        return user
    else:
        raise AuthError(u"Логин не соответствует паролю")
