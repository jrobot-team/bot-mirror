# -*- coding: utf-8 -*-
from _data_classes import (
    users_db,
    feed_db,
    Agent,
    ObjectApart,
    ObjectCommercial,
    ObjectHouse,
    ObjectArea
)

'''users_db.connect()
users_db.create_tables([
    Agent
])
users_db.close()'''

feed_db.connect()
feed_db.create_tables([
    ObjectApart,
    ObjectCommercial,
    ObjectHouse,
    ObjectArea
])
feed_db.close()