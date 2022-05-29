import telebot
import pandas as pd
import NLP
import prediction
import mapa
import subfunctions
from telebot import types
import config
import commands
import os
import sys
from requests.exceptions import ConnectionError, ReadTimeout
import time
import flask
#import requests
import logging

hi_flag = 0
qu_flag = 0
command_flag = 0
non_flag = 0
th_flag = 0
weater_flag = 0
b_flag = 0
qnon_flag = 0
mtext = ""

#______________________________________________________________________________
API_TOKEN = '5301739662:AAGWfetEsSQNUUiykxU9WL0pL5D2-9imlec'
APP_HOST = '127.0.0.1'
APP_PORT = '9000'
WEB_HOOK_URL = 'https://c94e-31-204-109-41.eu.ngrok.io'

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
boto = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)

@app.route('/',methods = ['POST'])
def webhook():
    if(flask.request.headers.get('content-type') == 'application/json'):
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        boto.process_new_updates([update])
        return ''
    else:
        flask.abort(403)