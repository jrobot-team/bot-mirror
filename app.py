# -*- coding: utf-8 -*-
import cherrypy
import telebot

import config
from _src_bot import bot
from _src_handler import Handler

handler = Handler()

@bot.message_handler(commands=['start', 'Start'])
def receive_command(message):
    handler.handle_command_message(message)

@bot.message_handler(func=lambda msg: True, content_types=['text'])
def receive_message(message):
    handler.handle_message(message)

@bot.callback_query_handler(func=lambda cb: True)
def receive_callback(cb):
    handler.handle_callback(cb)

# SERVER


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and 'content-type' in cherrypy.request.headers and cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

cherrypy.config.update({
    'server.socket_host': config.WEBHOOK_LISTEN,
    'server.socket_port': config.WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
    'server.ssl_private_key': config.WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), config.WEBHOOK_URL_PATH, {'/': {}})
