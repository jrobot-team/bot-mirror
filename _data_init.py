# -*- coding: utf-8 -*-
from _data_classes import (
    users_db,
    feed_db,
    Agent,
    Realty
)

'''users_db.connect()
users_db.create_tables([
    Agent
])
users_db.close()'''

feed_db.connect()
feed_db.create_tables([
    Realty
])
feed_db.close()
