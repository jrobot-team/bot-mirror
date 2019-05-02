# -*- coding: utf-8 -*-
import logging
import telebot
import config

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(config.token)

bot.remove_webhook()

bot.set_webhook(
    url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
    certificate=open(config.WEBHOOK_SSL_CERT, 'r'))