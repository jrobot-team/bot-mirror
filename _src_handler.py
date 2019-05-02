# -*- coding: utf-8 -*-
from telebot import types
from _strings import _s
from config import PARSE_MODE
from _data_service import data
from _src_bot import bot
import _src_admin as admin
import _src_agent as agent

reset = (
    '/start',
    '/Start',
    _s['agentmenu_filter'],
    _s['agentmenu_add'],
    _s['agentmenu_find'],
    _s['adminmenu_manage'],
    _s['adminmenu_stats']
)

class Handler(object):
    def handle_command_message(self, msg):
        role = data.idRole(msg.from_user.id)
        if msg.text == '/start':
            if role == 'admin':
                admin.start(msg)
            else:
                agent.start(msg)

    def handle_message(self, msg):
        pass

    def handle_callback(self, cb):
        bot.send_message(
            cb.from_user.id,
            cb.data
        )
