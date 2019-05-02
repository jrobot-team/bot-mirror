from telebot import types
from _strings import _s
from _src_consts import _c
from config import PARSE_MODE
from _src_bot import bot
from _data_service import data


def start(msg):
    replyKeys = types.ReplyKeyboardMarkup(row_width=1)
    replyKeys.add(
        types.KeyboardButton(_s['agentmenu_filter']),
        types.KeyboardButton(_s['agentmenu_add']),
        types.KeyboardButton(_s['agentmenu_find'])
    )
    bot.send_message(
        msg.chat.id,
        _s['agent_welcome'].format(name='[username]'),
        reply_markup=replyKeys,
        parse_mode=PARSE_MODE
    )
    bot.register_next_step_handler(
        msg,
        agwait_init
    )


def agwait_init(msg):
    print('ag wait handled')
    if msg.text == _s['agentmenu_filter']:
        keys = types.InlineKeyboardMarkup()
        buts = [
            types.InlineKeyboardButton(
                text=_s['filter_apart'],
                callback_data='ag_fng_ap'
                ),
            types.InlineKeyboardButton(
                text=_s['filter_commercial'],
                callback_data='ag_fng_co'
                ),
            types.InlineKeyboardButton(
                text=_s['filter_house'],
                callback_data='ag_fng_ho'
                ),
            types.InlineKeyboardButton(
                text=_s['filter_area'],
                callback_data='ag_fng_ar'
                )
        ]
        for i in buts:
            keys.add(i)
        bot.send_message(
            msg.chat.id,
            text=_s['filter_init_note'],
            reply_markup=keys,
            parse_mode=PARSE_MODE
        )
    else:
        bot.send_message(
            msg.chat.id,
            text=_s['dont_understand'],
            parse_mode=PARSE_MODE
        )
        bot.register_next_step_handler(
            msg,
            agwait_init
        )


def handle_callback(cb):
    args = cb.data.split('_')
    if args[1] == 'fng':
        cb_filtering(cb, args[2:])


def cb_filtering(cb, args):
    if args[0] == 'ap':
        if (len(args) == 1):
            #  вывести районы
            districts = data.get_apart_districts()
            keys = types.InlineKeyboardMarkup()
            for i in districts:
                keys.add(types.InlineKeyboardButton(
                        text=i[0],
                        callback_data='ag_fng_ap_{}'.format(i[1])
                    )
                )
            bot.send_message(
                cb.from_user.id,
                text=_s['filter_apart_district_note'],
                reply_markup=keys,
                parse_mode=PARSE_MODE
            )
        elif len(args) == 2:
            # вывести количества комнат в выбранном районе
            rooms = data.get_apart_rooms(args[1])
            keys = types.InlineKeyboardMarkup()
            for i in rooms:
                keys.add(types.InlineKeyboardButton(
                        text=i,
                        callback_data='ag_fng_ap_{0}_{1}'.format(args[1], i)
                    )
                )
            bot.send_message(
                cb.from_user.id,
                text=_s['filter_apart_rooms_note'],
                reply_markup=keys,
                parse_mode=PARSE_MODE
            )
        elif len(args) == 3:
            # вывести диапазоны цены
            keys = types.InlineKeyboardMarkup()
            for i in range(len(_c['prices_range'])):
                ran = _c['prices_range'][i]
                keys.add(types.InlineKeyboardButton(
                        text='{0} - {1}'.format(ran[0], ran[1]),
                        callback_data='ag_fng_ap_{0}_{1}_{2}'.format(args[1], args[2], i)
                    )
                )
            bot.send_message(
                cb.from_user.id,
                text=_s['filter_apart_prices_note'],
                reply_markup=keys,
                parse_mode=PARSE_MODE
            )
        elif len(args) == 4:
            # вывести диапазоны площади
            keys = types.InlineKeyboardMarkup()
            for i in range(len(_c['areas_range'])):
                ran = _c['areas_range'][i]
                keys.add(types.InlineKeyboardButton(
                        text='{0} - {1}'.format(ran[0], ran[1]),
                        callback_data='ag_fng_ap_{0}_{1}_{2}_{3}'.format(args[1], args[2], args[3], i)
                    )
                )
            bot.send_message(
                cb.from_user.id,
                text=_s['filter_apart_areas_note'],
                reply_markup=keys,
                parse_mode=PARSE_MODE
            )
        elif len(args) == 5:
            # вывести результаты выборки
            results = data.filter_apart(
                disthash=args[1],
                rooms=int(args[2]),
                pricesrangenum=int(args[3]),
                areasrangenum=int(args[4])
            )
            msg = '\n\n'.join(
                [
                    '\n'.join([i.district, i.rooms, i.price_value, i.area_value]) for i in j
                ] for j in results
            )
            bot.send_message(
                cb.from_user.id,
                text=msg
            )


def cb_filtering_apart(cb, args):
    pass


def cb_filtering_house(cb, args):
    pass


def cb_filtering_commercial(cb, args):
    pass


def cb_filtering_area(cb, args):
    pass
