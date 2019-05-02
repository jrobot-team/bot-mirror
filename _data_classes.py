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
    creation_date = DateTimeField()
    object_id = BigIntegerField()
    category = CharField()
    commercial_type = CharField()

    address = CharField()
    district = CharField()
    
    agent_name = CharField()
    agent_phone = CharField()
    images = CharField()
    price = CharField()

    rooms = IntegerField()
    floor = IntegerField()
    floors_total = IntegerField()

    area = CharField()
    living_space = CharField()
    kitchen_space = CharField()
    lot_area = IntegerField()
    
    description = TextField()

    class Meta:
        database = feed_db

class ObjectApart(Model):
    creation_date = DateTimeField() # Дата добавления
    object_id = BigIntegerField() # id
    address = CharField() # адрес
    district = CharField() # район
    agent_name = CharField()
    agent_phone = CharField()
    images = CharField() # список ссылок
    price = CharField() # цена
    rooms = IntegerField() # кол-во комнат
    floor = IntegerField() # этаж
    floors_total = IntegerField() # этажность
    area = CharField() # полная площадь
    living_space = CharField() # жилая плозадь
    kitchen_space = CharField() # площадь кухни 
    description = TextField() # описание

    class Meta:
        database = feed_db


class ObjectCommercial(Model):
    creation_date = DateTimeField() # Дата добавления
    object_id = BigIntegerField() # id
    address = CharField() # адрес
    district = CharField() # район
    agent_name = CharField() # id агента
    agent_phone = CharField()
    images = CharField()
    area = CharField()
    price = CharField() # цена
    floor = IntegerField() # этаж
    floors_total = IntegerField() # этажность
    description = TextField() # описание
    commercial_type = CharField() # тип сделки

    class Meta:
        database = feed_db


class ObjectHouse(Model):
    creation_date = DateTimeField() # дата добавления 
    object_id = BigIntegerField() # id
    address = CharField() # адрес
    #direction = CharField() # направление от города
    agent_name = CharField() # id агента
    agent_phone = CharField()
    images = CharField()
    price = CharField()
    rooms = IntegerField()
    category = CharField() # тип дома 
    floors_total = IntegerField() 
    area = IntegerField() 
    lot_area = IntegerField() # площадь участка
    #walls_material = CharField() # материал стен
    #distance = IntegerField() # расстояние от города
    description = TextField() # описание

    class Meta:
        database = feed_db


class ObjectArea(Model):
    add_date = DateTimeField()
    object_id = BigIntegerField()
    address = CharField()
    #direction = CharField()
    district = CharField() 
    #function = CharField() # назначение
    agent_name = CharField()
    agent_phone = CharField()
    images = CharField()
    price = IntegerField()
    lot_area = IntegerField() # площадь участка 
    #distance = IntegerField()
    description = TextField()

    class Meta:
        database = feed_db

