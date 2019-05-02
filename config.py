# -*- coding: utf-8 -*-

token = '879478335:AAHU2FLiUA_e6dOaUYdc5VDvYPgKlfdHOJs'

WEBHOOK_HOST = '212.80.217.60'
WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (token)


admin = (, )

TIMEZONE = 'Europe/Moscow'

PARSE_MODE = 'html'
