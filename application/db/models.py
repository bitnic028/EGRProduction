# coding=utf-8
# Created by Anton Dementev on 22.09.15 
from datetime import datetime

from peewee import Model, PostgresqlDatabase, PrimaryKeyField, CharField, BooleanField, ForeignKeyField, IntegerField, \
    TextField, DateField
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from server import settings

db = PostgresqlDatabase(
    settings.DB_NAME,
    user=settings.DB_ADMIN,
    password=settings.DB_PASSWORD
)
