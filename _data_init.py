from _data_classes import (
    db,
    Agent,
    ObjectApart,
    ObjectCommercial,
    ObjectHouse,
    ObjectArea
)

db.connect()
db.create_tables([
    Agent
])
db.close()
