# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from _data_classes import *

FEED_URL = 'https://base.kvartus.ru/reklama/xml/base/858/yrl.xml?fbclid=IwAR1q7AYKrtxLRJGxj8lDoBffanse6cEi2aB4LReinBNoyrAHEi3aRX6vWNA'


class Service(object):
    def idRole(self, _id):
        return 'agent'

    def updateFromFeed(self):
        try:
            xmldata = requests.get(FEED_URL).content
            root = ET.fromstring(xmldata)
        except Exception as e:
            print('get and parse XML error')
            return
        ns = {
            'ya': 'http://webmaster.yandex.ru/schemas/feed/realty/2010-06'
        }
        for offer in root.findall('ya:offer', ns):
            try:
                if offer.find('ya:type', ns).text != 'продажа':
                    continue

                obj_id = offer.get('internal-id')
                date = offer.find('ya:creation-date', ns).text
                date = datetime.strptime(date.split('T')[0], '%Y-%m-%d')
                cat = offer.find('ya:category', ns).text
                loc = offer.find('ya:location', ns)
                agent = offer.find('ya:sales-agent', ns)
                agent_name = agent.find('ya:name', ns).text
                agent_phone = agent.find('ya:phone', ns).text
                images = ' '.join([i.text for i in offer.findall('ya:image', ns)])
                price = offer.find('ya:price', ns)
                price_value = price.find('ya:value', ns)
                price_curr = price.find('ya:currency', ns)
                price = price_value.text
                if price_curr != None:
                    price += ' ' + price_curr.text
                description = offer.find('ya:description', ns).text
                
                if cat == 'квартира':
                    district = loc.find('ya:district', ns).text
                    address = loc.find('ya:address', ns).text
                    rooms = offer.find('ya:rooms', ns).text
                    floor = offer.find('ya:floor', ns).text
                    floors_total = offer.find('ya:floors-total', ns).text
                    x_area = offer.find('ya:area', ns)
                    x_livspace = offer.find('ya:living-space', ns)
                    x_kitspace = offer.find('ya:kitchen-space', ns)
                    area = ' '.join([x_area.find('ya:value', ns).text, x_area.find('ya:unit', ns).text])
                    living_space = ' '.join([x_livspace.find('ya:value', ns).text, x_livspace.find('ya:unit', ns).text])
                    kitchen_space = ' '.join([x_kitspace.find('ya:value', ns).text, x_kitspace.find('ya:unit', ns).text])
                elif cat == 'коммерческая':
                    comm_type = offer.find('ya:commercial-type', ns).text
                    x_area = offer.find('ya:area', ns)
                    area = ' '.join([x_area.find('ya:value', ns).text, x_area.find('ya:unit', ns).text])
                    floor = offer.find('ya:floor', ns).text
                    floors_total = offer.find('ya:floors-total', ns).text
                elif cat in (
                    'дом',
                    'дача',
                    'коттедж',
                    'дом с участком',
                    'часть дома',
                    'таунхаус',
                    'дуплекс'
                ):
                    address = loc.find('ya:address', ns).text
                    rooms = offer.find('ya:rooms', ns).text
                    floors_total = offer.find('ya:floors-total', ns).text
                    x_area = offer.find('ya:area', ns)
                    x_lotarea = offer.find('ya:lot-area', ns)
                    area = ' '.join([x_area.find('ya:value', ns).text, x_area.find('ya:unit', ns).text])
                    lot_area = ' '.join([x_lotarea.find('ya:value', ns).text, x_lotarea.find('ya:unit', ns).text])
                elif cat == 'участок':  
                    address = loc.find('ya:address', ns).text
                    district = loc.find('ya:district', ns).text
                    x_lotarea = offer.find('ya:lot-area', ns)
                    lot_area = ' '.join([x_lotarea.find('ya:value', ns).text, x_lotarea.find('ya:unit', ns).text])
            except Exception as e:
                print('parse offer error', str(e))


data = Service()
data.updateFromFeed()