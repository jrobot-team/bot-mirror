from telebot import types
from _strings import _s
from _src_consts import _c
from config import PARSE_MODE
from _src_bot import bot
from _data_service import data
import config


class AgentBot(object):
    id = 0

    state = -1
    # -1 - ничем не занят
    # 0 - подборка
    # 1 - добавление
    # 2 - поиск
    
    filters = []
    filter_num = 0
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
    # 2 - площадь

    filter_type = None
    realties = None

    current_message = None

    def start(self, id):
        self.id = id
        self.reset()
        self.reply()

    def reset(self):
        self.state = -1
        self.filter_num = -1
        self.realties = None
        self.filter_type = None
        self.current_message = None

    def command(self, msg):
        self.current_message = None
        self.reply()

    def message(self, msg):
        pass

    def callback(self, cb):
        print('agent call | ', cb.data, self.filter_num)
        if self.state == -1:
            if cb.data == 'start_filter':
                self.start_filter()
        elif self.state == 0:  # идёт подборка
            if cb.data == 'filter_reset':
                self.start_filter()
            elif cb.data == 'cancel':
                self.reset()
            elif cb.data == 'back':
                self.filter_back()
            elif cb.data == 'next':
                self.filter_next()
            elif cb.data == 'destroy_me':
                self.remove_message(cb.message)
            else:
                self.filter_tap(cb.data)
        self.reply()

    def start_filter(self):
        self.state = 0
        self.filter_num = -1
        self.filters = [TypesFilter()]
        print('start filter:   ', self.state, self.filter_num)

    def filter_tap(self, data):
        print('TAP --->   ', self.filter_type, self.filter_num, data)
        if self.filter_num == -1:  # выбор типа
            self.filter_type = data
            self.filter_next()
        else:
            if self.filter_num == len(self.filters):
                ans = self.realties.tap(data)
                if not isinstance(ans, bool) and ans is not None:
                    print('Agent: receive doc from realties')
                    self.send_document(ans)
            else:
                self.filters[self.filter_num].tap(data)
            '''
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
            '''

    def filter_next(self):
        if self.filter_num == -1:  # был выбор типа
            if self.filter_type == 'apart':
                self.filters = [
                    RoomsFilter(_c['apart_categories']),
                    PricesFilter(),
                    AreasFilter()
                ]
            if self.filter_type == 'comm':
                self.filters = [
                    CommTypesFilter(),
                    PricesFilter(),
                    AreasFilter()
                ]
            if self.filter_type == 'house':
                self.filters = [
                    CategoriesFilter(_c['house_categories']),
                    PricesFilter(),
                    AreasFilter()
                ]
            if self.filter_type == 'area':
                self.filters = [
                    PricesFilter(),
                    AreasFilter()
                ]
        elif self.filter_num == len(self.filters) - 1:
            self.realties = Realties(self.filter_type)
            self.realties.apply_filters(self.filters)
        self.filter_num += 1

    def filter_back(self):
        if self.filter_num == len(self.filters):
            if self.realties.tap('back'):
                self.filter_num -= 1
        else:
            self.filter_num -= 1
        if self.filter_num == -1:
            self.start_filter()

    def reply(self):
        if self.state == -1:
            self.start_message()
        elif self.state == 0:  # идёт подборка
            if self.filter_num < 0:
                m = self.filters[0].render_menu()
            else:
                if self.filter_num < len(self.filters):
                    m = self.filters[self.filter_num].render_menu()
                else:
                    m = self.realties.render_menu()
            self.send(text=m.text, keys=m.keys)

    def remove_message(self, msg):
        bot.delete_message(
            self.id,
            msg.message_id
        )

    def start_message(self):
        keys = types.InlineKeyboardMarkup()
        keys.row(
            types.InlineKeyboardButton(
                text=_s['agent_filter_start'],
                callback_data='start_filter'
            ),
            types.InlineKeyboardButton(
                text=_s['agent_append_start'],
                callback_data='start_filter'
            ),
            types.InlineKeyboardButton(
                text=_s['agent_search_start'],
                callback_data='start_filter'
            )
        )
        self.send(
            text=_s['agent_start_message'],
            keys=keys
        )

    def send_document(self, doc):
        print('Agent: sending doc')
        reply_id = None
        if self.current_message is not None:
            reply_id = self.current_message.message_id
        keys = types.InlineKeyboardMarkup()
        keys.add(types.InlineKeyboardButton(
            text=_s['destroy'],
            callback_data='destroy_me'
        ))
        bot.send_document(
            chat_id=self.id,
            data=doc,
            reply_to_message_id=reply_id,
            reply_markup=keys
        )

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


class Menu(object):
    def __init__(self, text, keys):
        self.text = text
        self.keys = keys


class TypesFilter(object):
    def render_menu(self):
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


class CommTypesFilter(object):
    def __init__(self):
        self.types = [
            {
                'checked': False,
                'name': i.commercial_type,
                'hash': str(hash(i.commercial_type))
            } for i in data.get_commercial_types()
        ]
        self.all = False

    def tap(self, data):
        if data == 'select_all':
            self.all = not self.all
        else:
            for i in self.types:
                if i['hash'] == data:
                    i['checked'] = not i['checked']
                    break

    def get_data(self):
        if self.all:
            return None
        res = []
        for i in self.types:
            if i['checked']:
                res += [i['name']]
        return res

    def render_menu(self):
        keys = types.InlineKeyboardMarkup()
        count = 0
        for i in self.types:
            if i['checked']:
                count += 1
            keys.add(types.InlineKeyboardButton(
                text=i['name'] if not i['checked'] else make_checked(i['name']),
                callback_data=i['hash']
            ))
        t = _s['filter_select_all']
        t = make_checked(t) if self.all else t
        keys.add(types.InlineKeyboardButton(
            text=t,
            callback_data='select_all'
        ))
        add_footer(
            keys,
            filter_reset=True,
            go_next=count > 0 or self.all
        )
        return Menu(
            _s['filter_commercial_types_note'],
            keys
        )


class CategoriesFilter(object):
    def __init__(self, type_categories):
        self.categories = [
            {
                'checked': False,
                'name': i.category,
                'hash': i.category_hash
            } for i in data.get_categories(type_categories)
        ]
        self.all = False

    def tap(self, data):
        if data == 'select_all':
            self.all = not self.all
        else:
            for i in self.categories:
                if i['hash'] == data:
                    i['checked'] = not i['checked']
                    break

    def get_data(self):
        if self.all:
            return None
        res = []
        for i in self.categories:
            if i['checked']:
                res += [i['name']]
        return res

    def render_menu(self):
        keys = types.InlineKeyboardMarkup()
        count = 0
        for i in self.categories:
            if i['checked']:
                count += 1
            keys.add(types.InlineKeyboardButton(
                text=i['name'] if not i['checked'] else make_checked(i['name']),
                callback_data=i['hash']
            ))
        t = _s['filter_select_all']
        t = make_checked(t) if self.all else t
        keys.add(types.InlineKeyboardButton(
            text=t,
            callback_data='select_all'
        ))
        add_footer(
            keys,
            filter_reset=True,
            go_next=count > 0 or self.all
        )
        return Menu(
            _s['filter_categories_note'],
            keys
        )


class PricesFilter(object):
    def __init__(self):
        self.data = _c['prices_ranges']
        self.selected = []
        self.all = False

    def tap(self, data):
        if data == 'select_all':
            self.all = not self.all
        else:
            n = int(data)
            if n in self.selected:
                self.selected.remove(n)
            else:
                self.selected.append(n)

    def get_data(self):
        if self.all:
            return None
        return [
            [_c['prices_ranges'][i][0], _c['prices_ranges'][i][1]] for i in self.selected
        ]

    def render_menu(self):
        keys = types.InlineKeyboardMarkup()
        for i in range(len(_c['prices_ranges'])):
            t = '{0} - {1}'.format(
                self.data[i][0], self.data[i][1]
            )
            if i in self.selected:
                t = make_checked(t)
            keys.add(types.InlineKeyboardButton(
                text=t,
                callback_data=str(i)
            ))
        t = _s['filter_select_all']
        t = make_checked(t) if self.all else t
        keys.add(types.InlineKeyboardButton(
            text=t,
            callback_data='select_all'
        ))
        add_footer(
            keys,
            filter_reset=True,
            go_next=len(self.selected) > 0 or self.all
        )
        return Menu(
            _s['filter_prices_note'],
            keys
        )


class AreasFilter(object):
    def __init__(self):
        self.data = _c['areas_ranges']
        self.selected = []
        self.all = False

    def tap(self, data):
        if data == 'select_all':
            self.all = not self.all
        else:
            n = int(data)
            if n in self.selected:
                self.selected.remove(n)
            else:
                self.selected.append(n)

    def get_data(self):
        if self.all:
            return None
        return [
            [_c['areas_ranges'][i][0], _c['areas_ranges'][i][1]] for i in self.selected
        ]

    def render_menu(self):
        keys = types.InlineKeyboardMarkup()
        for i in range(len(_c['areas_ranges'])):
            t = '{0} - {1}'.format(
                self.data[i][0], self.data[i][1]
            )
            if i in self.selected:
                t = make_checked(t)
            keys.add(types.InlineKeyboardButton(
                text=t,
                callback_data=str(i)
            ))
        t = _s['filter_select_all']
        t = make_checked(t) if self.all else t
        keys.add(types.InlineKeyboardButton(
            text=t,
            callback_data='select_all'
        ))
        add_footer(
            keys,
            filter_reset=True,
            go_next=len(self.selected) > 0 or self.all
        )
        return Menu(
            _s['filter_areas_note'],
            keys
        )


class RoomsFilter(object):
    def __init__(self, type_categories):
        self.rooms = [
            {
                'count': str(i.rooms),
                'checked': False
            } for i in data.get_rooms(type_categories)
        ]
        self.all = False

    def tap(self, data):
        if data == 'select_all':
            self.all = not self.all
        else:
            for i in self.rooms:
                if str(i['count']) == data:
                    i['checked'] = not i['checked']
                    break

    def get_data(self):
        if self.all:
            return None
        res = []
        for i in self.rooms:
            if i['checked']:
                res += [int(i['count'])]
        return res

    def render_menu(self):
        buts = []
        count = 0
        for i in self.rooms:
            t = i['count']
            if i['checked']:
                count += 1
            buts.append(types.InlineKeyboardButton(
                text=t if not i['checked'] else make_checked(t),
                callback_data=i['count']
            ))
        keys = types.InlineKeyboardMarkup()
        i = 0
        while i < len(buts) - 3:
            keys.row(*buts[i:i+3])
            i += 3
        if i < len(buts):
            keys.row(*buts[i:])
        t = _s['filter_select_all']
        t = make_checked(t) if self.all else t
        keys.add(types.InlineKeyboardButton(
            text=t,
            callback_data='select_all'
        ))
        add_footer(
            keys,
            filter_reset=True,
            go_next=count > 0 or self.all
        )
        return Menu(
            _s['filter_rooms_note'],
            keys
        )


class Realties(object):
    def __init__(self, _type):
        self.realties = []
        self.offset = -1
        self.show_mode = False
        self.show_realty = -1
        self.type = _type
        self.info = RealtyInfo(_type)

    def apply_filters(self, filters):
        rooms = None
        # dist_hashes = None
        categories = None
        comm_types = None
        prices = None
        areas = None
        for i in filters:
            filter_data = i.get_data()
            if isinstance(i, RoomsFilter):
                rooms = filter_data
            if isinstance(i, CategoriesFilter):
                categories = filter_data
            if isinstance(i, CommTypesFilter):
                comm_types = filter_data
            if isinstance(i, PricesFilter):
                prices = filter_data
            if isinstance(i, AreasFilter):
                areas = filter_data
        if categories is None:
            if self.type == 'area':
                categories = _c['area_categories']
            elif self.type == 'house':
                categories = _c['house_categories']
            elif self.type == 'comm':
                categories = _c['commercial_categories']
            else:
                categories = _c['apart_categories']
        print(comm_types)
        self.realties = data.apply_filter(
            prices=prices,
            areas=areas,
            area_field='lot_area_value' if self.type == 'area' else 'area_value',
            rooms=rooms,
            categories=categories,
            commercial_types=comm_types
        )
        print('-- founded:  ', len(self.realties))
        if len(self.realties) > 0:
            self.offset = 0

    def tap(self, data):
        if data == 'back':
            if self.show_mode:
                self.show_mode = False
            else:
                return True
        if 'rbut_' in data:
            id = int(data.split('_')[1])
            for i in self.realties:
                if i.realty_id == id:
                    self.set_show_mode(i)
                    break
        if data == 'all_images':
            return self.prepare_all_images(self.show_realty)
        if data == 'offset_plus':
            self.offset += config.PAGE_LEN
        if data == 'offset_minus':
            self.offset -= config.PAGE_LEN
        if self.offset < 0:
            self.offset = len(self.realties) - 1
        if self.offset >= len(self.realties):
            self.offset = 0
        n = self.offset // config.PAGE_LEN
        self.offset = n * config.PAGE_LEN
        return False

    def set_show_mode(self, r):
        self.show_realty = r
        self.show_mode = True

    def render_menu(self):
        keys = types.InlineKeyboardMarkup()
        if len(self.realties) == 0:
            text = _s['no_data']
        else:
            if self.show_mode:
                text = self.info.get(self.show_realty)
                self.add_images_button(keys, self.show_realty)
            else:
                text = _s['total_founded_objects'].format(len(self.realties))
                if len(self.realties) < config.PAGE_LEN:
                    for i in self.realties:
                        self.add_realty_button(keys, i)
                else:
                    for i in range(self.offset, self.offset + config.PAGE_LEN):
                        if i >= len(self.realties):
                            break
                        self.add_realty_button(
                            keys,
                            self.realties[i]
                        )
                    keys.row(*navigation_row())
        add_footer(keys, filter_reset=True)
        return Menu(text, keys)

    def add_images_button(self, keys, obj):
        if obj.images == '':
            return
        count = len(obj.images.split(' '))
        if count == 1:
            return
        keys.add(types.InlineKeyboardButton(
            text=_s['info_all_images_button'].format(count - 1),
            callback_data='all_images'
        ))

    def prepare_all_images(self, obj):
        print('Realties: preparing images')
        links = obj.images.split(' ')
        if len(links) > 0:
            return render_images_html(links)

    def add_realty_button(self, keys, obj):
        keys.add(types.InlineKeyboardButton(
            text=self.info.get_mini(obj),
            callback_data='rbut_' + str(obj.realty_id)
        ))


class RealtyInfo(object):
    def __init__(self, _type):
        self.type = _type

    def get(self, obj):
        if self.type == 'apart':
            return apart_info(obj)
        if self.type == 'comm':
            return commercial_info(obj)
        if self.type == 'house':
            return house_info(obj)
        if self.type == 'area':
            return area_info(obj)

    def get_mini(self, obj):
        return mini_info(obj)


def navigation_row():
    return [
        types.InlineKeyboardButton(
            text=_s['offset_minus'],
            callback_data='offset_minus'
        ),
        types.InlineKeyboardButton(
            text=_s['offset_plus'],
            callback_data='offset_plus'
        )
    ]


def add_footer(keys, filter_reset=False, go_next=False):
    keys.add(types.InlineKeyboardButton(
        text=_s['filter_reset'],
        callback_data='filter_reset'
    ))
    buts = [
        types.InlineKeyboardButton(
            text=_s['cancel'],
            callback_data='cancel'
        ),
        types.InlineKeyboardButton(
            text=_s['back'],
            callback_data='back'
        )
    ]
    if go_next:
        buts.append(types.InlineKeyboardButton(
            text=_s['next'],
            callback_data='next'
        ))
    
    keys.row(*buts)


def mini_info(obj):
    return ' '.join([
        obj.address,
        '|',
        render_price(obj.price_value),
        obj.price_currency
    ])


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
        _s['info_description'].format(obj.description),
        info_image(obj)
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
        _s['info_description'].format(obj.description),
        info_image(obj)
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
        _s['info_description'].format(obj.description),
        info_image(obj)
    ])


def area_info(obj):
    return '\n'.join([
        _s['info_category'].format(obj.category),
        _s['info_creation_date'].format(obj.creation_date),
        _s['info_district'].format(obj.district),
        _s['info_address'].format(obj.address),
        _s['info_price'].format(render_price(obj.price_value), obj.price_currency),
        _s['info_lot_area'].format(obj.lot_area_value, obj.lot_area_unit),
        _s['info_agent_name'].format(obj.agent_name),
        _s['info_agent_phone'].format(obj.agent_phone),
        _s['info_description'].format(obj.description),
        info_image(obj)
    ])


def info_image(obj):
    if obj.images != '':
        link = obj.images.split(' ')[0]
        return _s['info_image'].format(link)
    else:
        return _s['info_no_image']


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
    if p[-1] == '.':
        del p[-1]
    p.reverse()
    return ''.join(p)


def render_images_html(links):
    print('Nobody: rendering html')
    doc = open('images.html', 'w')
    hypertext = ''.join([
        _c['html_img_template'].format(i) for i in links
    ])
    hypertext = _c['html_template'].format(hypertext)
    print(hypertext)
    doc.write(hypertext)
    doc.close()
    return open('images.html')


def make_checked(t):
    return t + ' ✓'
