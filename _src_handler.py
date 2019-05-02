# -*- coding: utf-8 -*-
from telebot import types
from _strings import _s
from config import PARSE_MODE
from _data_service import data
from _src_bot import bot
import _src_admin as admin
import _src_agent as agent

reset = (
    '/reset',
    '/upd',
    _s['agentmenu_filter'],
    _s['agentmenu_add'],
    _s['agentmenu_find'],
    _s['adminmenu_manage'],
    _s['adminmenu_stats']
)


class Handler(object):
    def handle_command_message(self, msg):
        print('handle command')
        role = data.idRole(msg.from_user.id)
        if msg.text == '/reset':
            if role == 'admin':
                admin.start(msg)
            else:
                agent.start(msg)
        if msg.text == '/upd':
            data.updateFromFeed()

    def handle_message(self, msg):
        if msg.text in reset:
            role = data.idRole(msg.from_user.id)
            if role == 'admin':
                admin.start(msg)
            else:
                agent.start(msg)

    def handle_callback(self, cb):
        print('handle callback', cb.data)
        receiver = cb.data.split('_')[0]
        if receiver == 'ag':
            agent.handle_callback(cb)
