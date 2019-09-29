# What is the purpose of model.py?

import os

from peewee import Model, CharField, IntegerField
from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///mydatabase.db'))

class SavedTotal(Model):
    code = CharField(max_length=255, unique=True)
    value = IntegerField()

    class Meta:
        database = db