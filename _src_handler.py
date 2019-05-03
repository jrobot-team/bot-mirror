# -*- coding: utf-8 -*-
from _strings import _s
from _data_service import data
from _src_bot import bot
# import _src_admin as admin
from _src_agent import AgentBot


class Handler(object):
    bots = []

    def __init__(self):
        pass

    def command_start(self, message):
        print('--- handler command start/reset')
        for i in self.bots:
            if i.id == message.from_user.id:
                i.start(i.id)
                break
        else:
            new_bot = AgentBot()
            new_bot.start(message.from_user.id)
            self.bots.append(new_bot)

    def command_upd(self, message):
        data.updateFromFeed()

    def command_agent(self, message):
        for i in self.bots:
            print(i.id, message.from_user.id)
            if i.id == message.from_user.id:
                i.command(message)
                break

    def on_message(self, message):
        print('--- handler message')

    def on_callback(self, cb):
        print('--- callback', cb.data)
        for i in self.bots:
            print(i.id, cb.message.chat.id)
            if i.id == cb.message.chat.id:
                i.callback(cb)
                break


handler = Handler()


@bot.message_handler(commands=['start', 'reset'])
def command_start(msg):
    handler.command_start(msg)


@bot.message_handler(commands=['upd'])
def command_upd(msg):
    handler.command_upd(msg)


@bot.message_handler(commands=['filter', 'add', 'find'])
def command_agent(msg):
    handler.command_agent(msg)


@bot.message_handler(func=lambda msg: True, content_types=['text'])
def on_message(msg):
    handler.on_message(msg)
    print('--- handler message')


@bot.callback_query_handler(func=lambda cb: True)
def on_callback(cb):
    handler.on_callback(cb)
