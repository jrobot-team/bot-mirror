# -*- coding: utf-8 -*-
from peewee import (BigIntegerField, CharField, DateField, DateTimeField,
                    IntegerField, Model, TextField, FloatField)
from playhouse.sqlite_ext import SqliteExtDatabase

feed_db = SqliteExtDatabase(
    'data/feed_database.db',
    pragmas=(
        ('cache_size', -1024 * 64),
        ('journal_mode', 'wal'),
        ('foreign_keys', 1)
    )
)

users_db = SqliteExtDatabase(
    'data/users_database.db',
    pragmas=(
        ('cache_size', -1024 * 64),
        ('journal_mode', 'wal'),
        ('foreign_keys', 1)
    )
)


class Agent(Model):
    agent_id = BigIntegerField(default=0) # id
    name = CharField(default='') # Имя
    phone_number = CharField(default='') # номер в формате '79991112233'

    class Meta:
        database = users_db


class Realty(Model):
    realty_id = BigIntegerField()
    creation_date = DateTimeField()
    category = CharField(default='')
    commercial_type = CharField(default='')

    address = CharField(default='')
    district = CharField(default='')

    agent_name = CharField(default='')
    agent_phone = CharField(default='')
    images = CharField(default='')
    price_value = FloatField(default=0)
    price_currency = CharField(default='')

    rooms = IntegerField(default=0)
    floor = IntegerField(default=0)
    floors_total = IntegerField(default=0)

    area_value = FloatField(default=0)
    living_space_value = FloatField(default=0)
    kitchen_space_value = FloatField(default=0)
    lot_area_value = FloatField(default=0)
    area_unit = CharField(default='')
    living_space_unit = CharField(default='')
    kitchen_space_unit = CharField(default='')
    lot_area_unit = CharField(default='')

    description = TextField(default='')

    district_hash = CharField()
    category_hash = CharField()

    class Meta:
        database = feed_db
