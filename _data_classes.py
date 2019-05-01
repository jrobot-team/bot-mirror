# -*- coding: utf-8 -*-
from peewee import (BigIntegerField, CharField, DateField, DateTimeField,
                    IntegerField, Model, TextField)
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase(
    'data/database.db',
    pragmas=(
        ('cache_size', -1024 * 64),
        ('journal_mode', 'wal'),
        ('foreign_keys', 1)))


class Agent(Model):
    agent_id = BigIntegerField(default=0) # id
    name = CharField(default='') # Имя
    phone_number = CharField(default='') # номер в формате '79991112233'

    class Meta:
        database = db


class ObjectApart(Model):
    creation_date = DateField() # Дата добавления
    object_id = BigIntegerField() # id
    address = CharField() # адрес
    district = CharField() # район
    agent_id = BigIntegerField() # id агента
    #foto
    price = IntegerField() # цена
    rooms_count = IntegerField() # кол-во комнат
    floor = IntegerField() # этаж
    floors_count = IntegerField() # этажность
    full_area = IntegerField() # полная площадь
    live_area = IntegerField() # жилая плозадь
    kitchen_area = IntegerField() # площадь кухни 
    description = TextField() # описание

    class Meta:
        database = db


class ObjectCommercial(Model):
    add_date = DateField() # Дата добавления
    apart_id = BigIntegerField() # id
    address = CharField() # адрес
    district = CharField() # район
    agent_id = BigIntegerField() # id агента
    #foto
    price = IntegerField() # цена
    floor = IntegerField() # этаж
    floors_count = IntegerField() # этажность
    description = TextField() # описание
    deal_type = CharField() # тип сделки

    class Meta:
        database = db


class ObjectHouse(Model):
    add_date = DateField() # дата добавления 
    apart_id = BigIntegerField() # id
    address = CharField() # адрес
    direction = CharField() # направление от города
    agent_id = BigIntegerField() # id агента
    #foto
    price = IntegerField()
    rooms_count = IntegerField()
    house_type = CharField() # тип дома 
    floors_count = IntegerField() 
    full_area = IntegerField() 
    plot_area = IntegerField() # площадь участка
    walls_material = CharField() # материал стен
    distance = IntegerField() # расстояние от города
    description = TextField() # описание

    class Meta:
        database = db


class ObjectArea(Model):
    add_date = DateField()
    apart_id = BigIntegerField()
    address = CharField()
    direction = CharField()
    district = CharField() 
    function = CharField() # назначение
    agent_id = BigIntegerField()
    #foto
    price = IntegerField()
    plot_area = IntegerField() # площадь участка 
    distance = IntegerField()
    description = TextField()

    class Meta:
        database = db

