# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from _data_classes import Realty, Agent
from _src_consts import _c

FEED_URL = 'https://base.kvartus.ru/reklama/xml/base/7866/yrlmlsn.xml'


class Service(object):
    def idRole(self, _id):
        return 'agent'

    def updateFromFeed(self):
        try:
            xmldata = requests.get(FEED_URL).text
            root = ET.fromstring(xmldata)
        except Exception as e:
            print('get and parse XML error', str(e))
            return
        ns = {
            'ya': 'http://webmaster.yandex.ru/schemas/feed/realty/2010-06'
        }
        print('======== updating from feed')
        print('Deleted:   ', Realty.delete().execute())
        count = 0
        for offer in root.findall('ya:offer', ns):
            try:
                if offer.find('ya:type', ns).text != 'продажа':
                    continue

                realty = Realty()
                date = offer.find('ya:creation-date', ns).text
                realty.realty_id = offer.get('internal-id')
                realty.creation_date = datetime.strptime(date.split('T')[0], '%Y-%m-%d')
                agent = offer.find('ya:sales-agent', ns)
                realty.agent_name = agent.find('ya:name', ns).text
                realty.agent_phone = agent.find('ya:phone', ns).text
                cat = offer.find('ya:category', ns).text
                loc = offer.find('ya:location', ns)
                realty.category = cat
                realty.category_hash = hash(cat)
                realty.images = ' '.join([i.text for i in offer.findall('ya:image', ns)])
                price = offer.find('ya:price', ns)
                realty.price_value = price.find('ya:value', ns).text
                realty.price_currency = price.find('ya:currency', ns).text
                realty.description = offer.find('ya:description', ns).text

                if cat in _c['apart_categories']:
                    realty.address = loc.find('ya:address', ns).text
                    dist = loc.find('ya:district', ns).text
                    realty.district = dist
                    realty.district_hash = hash(dist)
                    realty.rooms = offer.find('ya:rooms', ns).text
                    realty.floor = offer.find('ya:floor', ns).text
                    realty.floors_total = offer.find('ya:floors-total', ns).text
                    x_area = offer.find('ya:area', ns)
                    x_livspace = offer.find('ya:living-space', ns)
                    x_kitspace = offer.find('ya:kitchen-space', ns)
                    realty.area_value = x_area.find('ya:value', ns).text
                    realty.area_unit = x_area.find('ya:unit', ns).text
                    realty.living_space_value = x_livspace.find('ya:value', ns).text
                    realty.living_space_unit = x_livspace.find('ya:unit', ns).text
                    realty.kitchen_space_value = x_kitspace.find('ya:value', ns).text
                    realty.kitchen_space_unit = x_kitspace.find('ya:unit', ns).text
                elif cat in _c['commercial_categories']:
                    realty.address = loc.find('ya:address', ns).text
                    dist = loc.find('ya:district', ns).text
                    realty.district = dist
                    realty.district_hash = hash(dist)
                    realty.commercial_type = offer.find('ya:commercial-type', ns).text
                    x_area = offer.find('ya:area', ns)
                    realty.area_value = x_area.find('ya:value', ns).text
                    realty.area_unit = x_area.find('ya:unit', ns).text
                    realty.floor = offer.find('ya:floor', ns).text
                    realty.floors_total = offer.find('ya:floors-total', ns).text
                elif cat in _c['house_categories']:
                    realty.address = loc.find('ya:address', ns).text
                    realty.rooms = offer.find('ya:rooms', ns).text
                    realty.floors_total = offer.find('ya:floors-total', ns).text
                    x_area = offer.find('ya:area', ns)
                    x_lotarea = offer.find('ya:lot-area', ns)
                    realty.area_value = x_area.find('ya:value', ns).text
                    realty.area_unit = x_area.find('ya:unit', ns).text
                    realty.lot_area_value = x_lotarea.find('ya:value', ns).text
                    realty.lot_area_unit = x_lotarea.find('ya:unit', ns).text
                elif cat in _c['area_categories']:
                    realty.address = loc.find('ya:address', ns).text
                    dist = loc.find('ya:district', ns).text
                    realty.district = dist
                    realty.district_hash = hash(dist)
                    x_lotarea = offer.find('ya:lot-area', ns)
                    realty.lot_area_value = x_lotarea.find('ya:value', ns).text
                    realty.lot_area_unit = x_lotarea.find('ya:unit', ns).text
                count += 1
                realty.save(force_insert=True)
            except Exception as e:
                print('Parsing error:  ', str(e))
        print('Parsed:   ', count)
        count = 0
        for i in Realty.select():
            count += 1
        print('In Database:   ', count)

    def get_districts(self, category):
        query = Realty.select(Realty.district, Realty.district_hash).distinct().where(
            Realty.category in category
        )
        return query

    def get_categories(self, category):
        query = Realty.select(Realty.category, Realty.category_hash).distinct().where(
            Realty.category in category
        )
        return query

    def get_rooms(self, category, hashes):
        query = Realty.select(Realty.rooms).distinct().where(
            Realty.category in category
            and Realty.district_hash in hashes
        )
        return query

    def filter_apart(self, disthashes, rooms, prices, areas):
        _prices = []
        _areas = []
        for i in prices:
            _prices += [i.price_value for i in Realty.select(Realty.price_value).distinct().where(i[0] <= Realty.price_value <= i[1])] 
        for i in areas:
            _areas += [i.area_value for i in Realty.select(Realty.area_value).distinct().where(i[0] <= Realty.area_value <= i[1])]
        query = Realty.select().where(
            Realty.district_hash in disthashes
            and Realty.rooms in rooms
            and Realty.price_value in prices
            and Realty.area_value in areas
        )
        return query


data = Service()

if __name__ == '__main__':
    data.updateFromFeed()
