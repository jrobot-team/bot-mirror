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
        total_count = 0
        for offer in root.findall('ya:offer', ns):
            try:
                total_count += 1
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
                realty.save(force_insert=True)
                count += 1
            except Exception as e:
                print('Parsing error:  ', str(e))
        print('Total founded:   ', total_count)
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
        return Realty.select(
            Realty.category, Realty.category_hash
        ).distinct().where(
            Realty.category.in_(category)
        )

    def get_commercial_types(self):
        query = Realty.select(Realty.commercial_type).distinct()
        return query

    def get_rooms(self, category):
        return Realty.select(Realty.rooms).distinct().where(
            Realty.category.in_(category)
        ).order_by(Realty.rooms)

    def get_all(self):
        return Realty.select()

    def get_all_lots(self):
        return Realty.select().where(Realty.category_hash.in_([str(hash(i)) for i in _c['area_categories']]))

    def apply_filter(
        self,
        prices=None,
        areas=None,
        area_field='area_value',
        rooms=None,
        categories=None,
        commercial_types=None
    ):
        _prices = []
        _areas = []
        query = Realty.select(
            Realty.price_value, 
            self.area_field(Realty, area_field)
        )
        for i in query:
            if prices is None:
                _prices += [i.price_value]
            else:
                for j in prices:
                    if j[0] <= i.price_value <= j[1]:
                        _prices += [i.price_value]
            value = self.area_field(i, area_field)
            if areas is None:
                _areas += [value]
            else:
                for j in areas:
                    if j[0] <= value <= j[1]:
                        _areas += [value]
        args = [
            Realty.price_value.in_(_prices),
            self.area_field(Realty, area_field).in_(_areas)
        ]
        if rooms is not None:
            args += [Realty.rooms.in_(rooms)]
        if categories is not None:
            args += [Realty.category.in_(categories)]
        if commercial_types is not None:
            args += [Realty.commercial_type.in_(commercial_types)]
        return Realty.select().where(*args)

    def area_field(self, obj, field):
        if field == 'area_value':
            return obj.area_value
        if field == 'lot_area_value':
            return obj.lot_area_value


data = Service()

if __name__ == '__main__':
    data.updateFromFeed()
