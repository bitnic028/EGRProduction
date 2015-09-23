# coding=utf-8
# Created by Anton Dementev on 22.09.15 
from datetime import datetime


class DateFormats:
    short = u"{0}-{1}-{2}"
    long = u"{0} {1} {2} г."


MONTHES = (
    u"января",
    u"февраля",
    u"марта",
    u"апреля",
    u"мая",
    u"июня",
    u"июля",
    u"августа",
    u"сентября",
    u"октября",
    u"ноября",
    u"декабря",
)


def string_from_date(date, format_type):
    if format_type == u"short1":
        return date.strftime("%d-%m-%Y")
    elif format_type == u"short2":
        return DateFormats.short.format(date.day, date.month, date.year)

    else:
        return DateFormats.long.format(date.day, MONTHES[date.month - 1], date.year)


def rounded_date(date):
    return datetime.strptime(string_from_date(date, u"short2").encode("utf8"), "%d-%m-%Y")
