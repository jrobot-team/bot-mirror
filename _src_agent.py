from telebot import types
from _strings import _s
from _src_consts import _c
from config import PARSE_MODE
from _src_bot import bot
from _data_service import data


class AgentBot(object):
    id = 0

    state = -1
    # -1 - ничем не занят
    # 0 - подборка
    # 1 - добавление
    # 2 - поиск

    filter_state = 0
    # 0 - выбор типа объекта
    # APART
    # 1 - выбор района
    # 2 - выбор количества комнат
    # 3 - выбор диапазона цены
    # 4 - выбор диапазона площади
    # COMMERCIAL
    # 1 - район
    # 2 - цена
    # 3 - площадь
    # HOUSE
    # 1 - тип
    # 2 - цена
    # 3 - площадь
    # AREA
    # 1 - цена
    # 1 - площадь

    filter_type = None
    districts = []
    rooms = []
    prices = []
    areas = []

    current_message = None

    def start(self, id):
        self.id = id
        self.reset()
        self.reply()

    def reset(self):
        self.state = -1
        self.filter_state = -1
        self.districts = []
        self.categories = []
        self.rooms = []
        self.prices = []
        self.areas = []
        self.filter_type = None
        self.current_message = None

    def command(self, msg):
        self.current_message = None
        if msg.text == '/filter':
            self.state = 0
            self.filter_state = 0
        self.reply()

    def message(self, msg):
        pass

    def callback(self, cb):
        print('call', cb.data)
        if self.state == 0:  # идёт подборка
            if cb.data == 'cancel':
                self.reset()
            elif cb.data == 'back':
                self.filter_back()
            elif cb.data == 'next':
                self.filter_next()
            else:
                self.filter_tap(cb.data)
        self.reply()

    def filter_tap(self, data):
        if self.filter_state == 0:  # выбор типа
            self.filter_type = data
            self.filter_next()
        else:
            on_showing = False
            if self.filter_type == 'apart':
                if self.filter_state == 1:  # выбор района
                    for i in self.districts:
                        if data == i['hash']:
                            i['checked'] = not i['checked']
                if self.filter_state == 2:  # выбор количества комнат
                    for i in self.rooms:
                        if data == str(i['count']):
                            i['checked'] = not i['checked']
                if self.filter_state == 3:  # выбор цен
                    n = int(data)
                    if n in self.prices:
                        self.prices.remove(n)
                    else:
                        self.prices.append(n)
                if self.filter_state == 4:  # выбор площади
                    n = int(data)
                    if n in self.areas:
                        self.areas.remove(n)
                    else:
                        self.areas.append(n)
                if self.filter_state == 5:  # просмотр объектов
                    on_showing = True
            if self.filter_type == 'comm':
                if self.filter_state == 1:  # выбор района
                    for i in self.districts:
                        if data == i['hash']:
                            i['checked'] = not i['checked']
                if self.filter_state == 2:  # выбор цен
                    n = int(data)
                    if n in self.prices:
                        self.prices.remove(n)
                    else:
                        self.prices.append(n)
                if self.filter_state == 3:  # выбор площади
                    n = int(data)
                    if n in self.areas:
                        self.areas.remove(n)
                    else:
                        self.areas.append(n)
                if self.filter_state == 4:  # просмотр объектов
                    on_showing = True
            if self.filter_type == 'house':
                if self.filter_state == 1:  # выбор типа
                    for i in self.categories:
                        if data == i['hash']:
                            i['checked'] = not i['checked']
                if self.filter_state == 2:  # выбор цен
                    n = int(data)
                    if n in self.prices:
                        self.prices.remove(n)
                    else:
                        self.prices.append(n)
                if self.filter_state == 3:  # выбор площади
                    n = int(data)
                    if n in self.areas:
                        self.areas.remove(n)
                    else:
                        self.areas.append(n)
                if self.filter_state == 4:  # просмотр объектов
                    on_showing = True
            if self.filter_type == 'area':
                if self.filter_state == 1:  # выбор цен
                    n = int(data)
                    if n in self.prices:
                        self.prices.remove(n)
                    else:
                        self.prices.append(n)
                if self.filter_state == 2:  # выбор площади
                    n = int(data)
                    if n in self.areas:
                        self.areas.remove(n)
                    else:
                        self.areas.append(n)
                if self.filter_state == 3:  # просмотр объектов
                    on_showing = True
            if on_showing:
                if data == 'another_realty':
                    if self.current_realty_num == len(self.realties) - 1:
                        self.current_realty_num = 0
                    else:
                        self.current_realty_num += 1
                if data == 'another_image':
                    if self.current_image_num == len(self.images) - 1:
                        self.current_image_num = 0
                    else:
                        self.current_image_num += 1

    def filter_next(self):
        if self.filter_type == 'apart':
            if self.filter_state == 0:  # сейчас был выбор типа, далее районы
                self.request_districts(_c['apart_categories'])
                self.filter_state += 1
            elif self.filter_state == 1:  # сейчас районы, далее комнаты
                hashes = [i['hash'] for i in self.districts]
                self.request_rooms(_c['apart_categories'], hashes)
                self.filter_state += 1
            elif self.filter_state == 2:
                self.prices = []
                self.filter_state += 1
            elif self.filter_state == 3:
                self.areas = []
                self.filter_state += 1
            elif self.filter_state == 4:  # подготовить результаты
                self.filter_apply()
                self.filter_state += 1
        if self.filter_type == 'comm':
            if self.filter_state == 0:  # сейчас был выбор типа, далее районы
                self.request_districts(_c['commercial_categories'])
                self.filter_state += 1
            elif self.filter_state == 1:  # сейчас районы, далее цены
                self.prices = []
                self.filter_state += 1
            elif self.filter_state == 2:
                self.areas = []
                self.filter_state += 1
            elif self.filter_state == 3:  # подготовить результаты
                self.filter_apply()
                self.filter_state += 1
        if self.filter_type == 'house':
            if self.filter_state == 0:  # сейчас был выбор типа, далее районы
                self.request_categoties(_c['house_categories'])
                self.filter_state += 1
            elif self.filter_state == 1:
                self.prices = []
                self.filter_state += 1
            elif self.filter_state == 2:
                self.areas = []
                self.filter_state += 1
            elif self.filter_state == 3:  # подготовить результаты
                self.filter_apply()
                self.filter_state += 1
        if self.filter_type == 'area':
            if self.filter_state == 0:
                self.prices = []
                self.filter_state += 1
            elif self.filter_state == 1:
                self.areas = []
                self.filter_state += 1
            elif self.filter_state == 2:
                self.filter_apply()
                self.filter_state += 1

    def filter_back(self):
        if self.filter_state > 0:
            self.filter_state -= 1

    def reply(self):
        if self.state == -1:
            self.send(_s['agent_welcome'])
        elif self.state == 0:  # идёт подборка
            if self.filter_state == 0:  # отправить меню типов
                m = self.menu_filter_types()
                self.send(m.text, keys=m.keys)
            else:
                show_info = False
                if self.filter_type == 'apart':
                    if self.filter_state == 1:  # отправить меню районов
                        m = self.menu_filter_districts()
                        self.send(text=m.text, keys=m.keys)
                    elif self.filter_state == 2:  # меню комнат
                        m = self.menu_filter_rooms()
                        self.send(text=m.text, keys=m.keys)
                    elif self.filter_state == 3:  # меню цен
                        m = self.menu_filter_prices()
                        self.send(text=m.text, keys=m.keys)
                    elif self.filter_state == 4:  # меню площадей
                        m = self.menu_filter_areas()
                        self.send(text=m.text, keys=m.keys)
                    elif self.filter_state == 5:  # показ найденного объекта
                        show_info = True
                if self.filter_type == 'comm':
                    if self.filter_state == 1:  # отправить меню районов
                        m = self.menu_filter_districts()
                        self.send(text=m.text, keys=m.keys)
                    elif self.filter_state == 2:
                        m = self.menu_filter_prices()
                        self.send(text=m.text, keys=m.keys)
                    elif self.filter_state == 3:
                        m = self.menu_filter_areas()
                        self.send(text=m.text, keys=m.keys)
                    elif self.filter_state == 4:  # показ найденного объекта
                        show_info = True
                if self.filter_type == 'house':
                    if self.filter_state == 1:  # отправить меню районов
                        m = self.menu_filter_categories()
                        self.send(text=m.text, keys=m.keys)
                    elif self.filter_state == 2:
                        m = self.menu_filter_prices()
                        self.send(text=m.text, keys=m.keys)
                    elif self.filter_state == 3:
                        m = self.menu_filter_areas()
                        self.send(text=m.text, keys=m.keys)
                    elif self.filter_state == 4:  # показ найденного объекта
                        show_info = True
                if self.filter_type == 'comm':
                    if self.filter_state == 1:
                        m = self.menu_filter_prices()
                        self.send(text=m.text, keys=m.keys)
                    elif self.filter_state == 2:
                        m = self.menu_filter_areas()
                        self.send(text=m.text, keys=m.keys)
                    elif self.filter_state == 3:  # показ найденного объекта
                        show_info = True
                if show_info:
                    m = self.menu_realty_info()
                    self.send(text=m.text, keys=m.keys)

    def send(self, text, keys=None):
        if self.current_message is not None:
            bot.edit_message_text(
                chat_id=self.id,
                message_id=self.current_message.message_id,
                text=text,
                reply_markup=keys,
                parse_mode=PARSE_MODE
            )
        else:
            self.current_message = bot.send_message(
                self.id,
                text=text,
                parse_mode=PARSE_MODE,
                reply_markup=keys
            )

    def menu_filter_types(self):
        keys = types.InlineKeyboardMarkup()
        buts = [
            types.InlineKeyboardButton(
                text=_s['filter_apart'],
                callback_data='apart'
            ),
            types.InlineKeyboardButton(
                text=_s['filter_commercial'],
                callback_data='comm'
            ),
            types.InlineKeyboardButton(
                text=_s['filter_house'],
                callback_data='house'
            ),
            types.InlineKeyboardButton(
                text=_s['filter_area'],
                callback_data='area'
            ),
            types.InlineKeyboardButton(
                text=_s['cancel'],
                callback_data='cancel'
            )
        ]
        for i in buts:
            keys.add(i)
        return Menu(
            _s['filter_types_note'],
            keys
        )

    def menu_filter_districts(self):
        keys = types.InlineKeyboardMarkup()
        count = 0
        for i in self.districts:
            if i['checked']:
                count += 1
            keys.add(types.InlineKeyboardButton(
                text=i['name'] if not i['checked'] else self.make_checked(i['name']),
                callback_data=i['hash']
            ))
        keys.row(*self.menu_filter_footer_row(count > 0))
        return Menu(
            _s['filter_districts_note'],
            keys
        )

    def menu_filter_categories(self):
        keys = types.InlineKeyboardMarkup()
        count = 0
        for i in self.categories:
            if i['checked']:
                count += 1
            keys.add(types.InlineKeyboardButton(
                text=i['name'] if not i['checked'] else self.make_checked(i['name']),
                callback_data=i['hash']
            ))
        keys.row(*self.menu_filter_footer_row(count > 0))
        return Menu(
            _s['filter_categories_note'],
            keys
        )

    def menu_filter_rooms(self):
        print('render menu rooms:', str(self.rooms))
        buts = []
        count = 0
        for i in self.rooms:
            t = i['count']
            if i['checked']:
                count += 1
            buts.append(types.InlineKeyboardButton(
                text=t if not i['checked'] else self.make_checked(t),
                callback_data=i['count']
            ))
        keys = types.InlineKeyboardMarkup()
        i = 0
        while i < len(buts) - 3:
            keys.row(*buts[i:i+3])
            i += 3
        if i < len(buts):
            keys.row(*buts[i:])
        keys.row(*self.menu_filter_footer_row(count > 0))
        return Menu(
            _s['filter_rooms_note'],
            keys
        )

    def menu_filter_prices(self):
        keys = types.InlineKeyboardMarkup()
        for i in range(len(_c['prices_ranges'])):
            t = '{0} - {1}'.format(
                _c['prices_ranges'][i][0], _c['prices_ranges'][i][1]
            )
            if i in self.prices:
                t = self.make_checked(t)
            keys.add(types.InlineKeyboardButton(
                text=t,
                callback_data=str(i)
            ))
        keys.row(*self.menu_filter_footer_row(len(self.prices) > 0))
        return Menu(
            _s['filter_prices_note'],
            keys
        )

    def menu_filter_areas(self):
        keys = types.InlineKeyboardMarkup()
        for i in range(len(_c['areas_ranges'])):
            t = '{0} - {1}'.format(
                _c['areas_ranges'][i][0], _c['areas_ranges'][i][1]
            )
            if i in self.areas:
                t = self.make_checked(t)
            keys.add(types.InlineKeyboardButton(
                text=t,
                callback_data=str(i)
            ))
        keys.row(*self.menu_filter_footer_row(len(self.areas) > 0))
        return Menu(
            _s['filter_areas_note'],
            keys
        )

    def menu_realty_info(self):
        text = self.realty_info()
        keys = types.InlineKeyboardMarkup()
        keys.add(types.InlineKeyboardButton(
            text=_s['another_realty'],
            callback_data='another_realty'
        ))
        if len(self.images) > 0:
            keys.add(types.InlineKeyboardButton(
                text=_s['another_image'],
                callback_data='another_image'
            ))
        keys.row(*self.menu_filter_footer_row())
        return Menu(text, keys)

    def make_checked(self, text):
        return text + ' +'

    def menu_filter_footer_row(self, _next=False):
        footer = [
            types.InlineKeyboardButton(
                text=_s['cancel'],
                callback_data='cancel'
            ),
            types.InlineKeyboardButton(
                text=_s['back'],
                callback_data='back'
            ),
        ]
        if _next > 0:
            footer.append(types.InlineKeyboardButton(
                text=_s['next'],
                callback_data='next'
            ))
        return footer

    def realty_info(self):
        if self.current_realty_num < 0 or self.current_realty_num >= len(self.realties):
            return _s['no data']
        obj = self.realties[self.current_realty_num]
        if obj.category in _c['apart_categories']:
            info = apart_info(obj)
        elif obj.category in _c['commercial_categories']:
            info = commercial_info(obj)
        elif obj.category in _c['house_categories']:
            info = house_info(obj)
        elif obj.category in _c['area_categories']:
            info = area_info(obj)
        else:
            info = '|=---= ~ =---=|'
        if len(self.images) > 0:
            if self.current_image_num >= 0 and self.current_image_num < len(self.images):
                info += '\n' + self.images[self.current_image_num]
        return info

    def filter_apply(self):
        print(str(self.rooms))
        res = data.filter_apart(
            disthashes=[i['hash'] for i in self.districts],
            rooms=[int(i['count']) for i in self.rooms],
            prices=[[_c['prices_ranges'][i][0], _c['prices_ranges'][i][0]] for i in self.prices],
            areas=[[_c['areas_ranges'][i][0], _c['areas_ranges'][i][0]] for i in self.areas]
        )
        self.realties = res
        self.current_realty_num = 0
        self.images = ''#res.images.split('&')
        self.current_image_num = 0

    def request_districts(self, cat):
        self.districts = [
            {
                'checked': False,
                'name': i.district,
                'hash': i.district_hash
            } for i in data.get_districts(cat)
        ]

    def request_rooms(self, cat, hashes):
        self.rooms = [
            {
                'count': str(i.rooms),
                'checked': False
            } for i in data.get_rooms(_c['apart_categories'], hashes)
        ]

    def request_categoties(self, cat):
        self.categories = [
            {
                'checked': False,
                'name': i.category,
                'hash': i.category_hash
            } for i in data.get_categories(cat)
        ]


class Menu(object):
    def __init__(self, text, keys):
        self.text = text
        self.keys = keys


def apart_info(obj):
    return '\n'.join([
        _s['info_category'].format(obj.category),
        _s['info_creation_date'].format(obj.creation_date),
        _s['info_district'].format(obj.district),
        _s['info_address'].format(obj.address),
        _s['info_price'].format(render_price(obj.price_value), obj.price_currency),
        _s['info_rooms'].format(obj.rooms),
        _s['info_floor'].format(obj.floor),
        _s['info_floors_total'].format(obj.floors_total),
        _s['info_area'].format(obj.area_value, obj.area_unit),
        _s['info_living_space'].format(obj.living_space_value, obj.living_space_unit),
        _s['info_kitchen_space'].format(obj.kitchen_space_value, obj.kitchen_space_unit),
        _s['info_agent_name'].format(obj.agent_name),
        _s['info_agent_phone'].format(obj.agent_phone),
        _s['info_description'].format(obj.description)
    ])

def commercial_info(obj):
    return '\n'.join([
        _s['info_category'].format(obj.category),
        _s['info_creation_date'].format(obj.creation_date),
        _s['info_commercial_type'].format(obj.commercial_type),
        _s['info_district'].format(obj.district),
        _s['info_address'].format(obj.address),
        _s['info_price'].format(render_price(obj.price_value), obj.price_currency),
        _s['info_floor'].format(obj.floor),
        _s['info_floors_total'].format(obj.floors_total),
        _s['info_area'].format(obj.area_value, obj.area_unit),
        _s['info_agent_name'].format(obj.agent_name),
        _s['info_agent_phone'].format(obj.agent_phone),
        _s['info_description'].format(obj.description)
    ])

def house_info(obj):
    return '\n'.join([
        _s['info_category'].format(obj.category),
        _s['info_creation_date'].format(obj.creation_date),
        _s['info_district'].format(obj.district),
        _s['info_address'].format(obj.address),
        _s['info_price'].format(render_price(obj.price_value), obj.price_currency),
        _s['info_rooms'].format(obj.rooms),
        _s['info_floors_total'].format(obj.floors_total),
        _s['info_area'].format(obj.area_value, obj.area_unit),
        _s['info_lot_area'].format(obj.lot_area_value, obj.lot_area_unit),
        _s['info_agent_name'].format(obj.agent_name),
        _s['info_agent_phone'].format(obj.agent_phone),
        _s['info_description'].format(obj.description)
    ])

def area_info(obj):
    return '\n'.join([
        _s['info_category'].format(obj.category),
        _s['info_creation_date'].format(obj.creation_date),
        _s['info_district'].format(obj.district),
        _s['info_address'].format(obj.address),
        _s['info_price'].format(render_price(obj.price_value), obj.price_currency),
        _s['info_lot_area'].format(obj.area_value, obj.area_unit),
        _s['info_agent_name'].format(obj.agent_name),
        _s['info_agent_phone'].format(obj.agent_phone),
        _s['info_description'].format(obj.description)
    ])

def render_price(num):
    s = list(str(int(num)))
    s.reverse()
    p = []
    n = 0
    for i in s:
        p.append(i)
        if n == 2:
            p.append('.')
            n = 0
        else:
            n += 1
    p.reverse()
    return ''.join(p)
