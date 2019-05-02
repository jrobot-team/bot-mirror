# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from _data_classes import Realty, Agent
from _src_consts import _c

FEED_URL = 'https://base.kvartus.ru/reklama/xml/base/858/yrl.xml?fbclid=IwAR1q7AYKrtxLRJGxj8lDoBffanse6cEi2aB4LReinBNoyrAHEi3aRX6vWNA'


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
        Realty.delete().execute()
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
                realty.price_value = price.find('ya:value', ns)
                realty.price_currency = price.find('ya:currency', ns)
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

                realty.save()
            except Exception as e:
                pass

    def get_apart_districts(self):
        query = Realty.select(
            Realty.district, Realty.district_hash
        ).distinct().where(
            Realty.category in _c['apart_categories']
        )
        return [(i.district, i.district_hash) for i in query]

    def get_apart_rooms(self, disthash):
        query = Realty.select(Realty.rooms).distinct().where(
            Realty.category in _c['apart_categories'] and Realty.district_hash == disthash
        )
        return [i.rooms for i in query]
    
    def filter_apart(disthash, rooms, prn, arn):
        minprice = _c['price_ranges'][0]
        maxprice = _c['price_ranges'][1]
        minarea = _c['areas_ranges'][0]
        maxarea = _c['areas_ranges'][1]
        query = Realty.select().where(
            Realty.district_hash == disthash
            and Realty.rooms == rooms
            and minprice <= Realty.price_value <= maxprice
            and minarea <= Realty.area_value <= maxarea
        )
        return query


data = Service()
