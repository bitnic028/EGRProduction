# coding=utf-8
# Created by Anton Dementev on 22.09.15 
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

LOGS_DIR = BASE_DIR + "/logs"
STATIC_DIR = BASE_DIR + "/static"
TEMPLATE_DIR = BASE_DIR + "/application/templates"

DB_NAME = "egr_production"
DB_ADMIN = "egr_admin"
DB_PASSWORD = "firstclient"
HASH_SALT = "abdurahman ibn hattab"

DOMAIN = ""
ADMIN_REDIRECT = "/"
CLIENT_REDIRECT = "/"

APP_SETTINGS = dict(
    cookie_secret="0f362f71b9b22354c730644281638f866cf2ea2a",
    template_path=TEMPLATE_DIR,
    static_path=STATIC_DIR,
    xsrf_cookies=True,
    default_handler_args=dict(status_code=404)
)

MONTHES_LONG = (
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

MONTHES_SHORT = (
    u"янв",
    u"фев",
    u"мар",
    u"апр",
    u"май",
    u"июн",
    u"июл",
    u"авг",
    u"сен",
    u"окт",
    u"ноя",
    u"дек",
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'access': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR + "/egr_access.log",
            'maxBytes': 50000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        'app': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR + "/egr_app.log",
            'maxBytes': 50000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        'general': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR + "/egr_general.log",
            'maxBytes': 50000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR + "/egr_debug.log",
            'maxBytes': 50000,
            'backupCount': 3,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        "handlers": {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["debug", "console"]
        },
        "tornado.access": {
            "level": "INFO",
            "propagate": False,
            "handlers": ["access", "console"]
        },
        "tornado.application": {
            "level": "INFO",
            "propagate": False,
            "handlers": ["app", "console"]
        },
        "tornado.general": {
            "level": "INFO",
            "propagate": False,
            "handlers": ["general", "console"]
        },
    }
}
