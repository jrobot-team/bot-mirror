# -*- coding: utf-8 -*-
from telebot import types
from _strings import _s
from config import PARSE_MODE
from _src_bot import bot


def start(msg):
    '''replyKeys = types.ReplyKeyboardMarkup(row_width=1)
    replyKeys.add(
        types.KeyboardButton(_s['filter_objects_but']),
        types.KeyboardButton(_s['add_buyer_but']),
        types.KeyboardButton(_s['find_buyer_but'])
    )'''
    bot.send_message(
        msg.chat.id,
        _s['admin_welcome'],
        #reply_markup=replyKeys,
        parse_mode=PARSE_MODE
    )