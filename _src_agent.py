from telebot import types
from _strings import _s
from config import PARSE_MODE
from _src_bot import bot


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
        agent_start
    )


def agent_start(msg):
    if msg.text == _s['agentmenu_filter']:
        keys = types.InlineKeyboardMarkup()
        buts = [
            types.InlineKeyboardButton(
                text=_s['filter_apart'],
                callback_data='ap'
                ),
            types.InlineKeyboardButton(
                text=_s['filter_commercial'],
                callback_data='co'
                ),
            types.InlineKeyboardButton(
                text=_s['filter_house'],
                callback_data='ho'
                ),
            types.InlineKeyboardButton(
                text=_s['filter_area'],
                callback_data='ar'
                )
        ]
        for i in buts:
            keys.add(i)
        bot.send_message(
            msg.chat.id,
            text=_s['filter_init'],
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
            agent_start
        )
