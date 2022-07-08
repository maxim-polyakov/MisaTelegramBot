import telebot
import pandas as pd
from NLP import Models
from NLP import Predictors
from NLP import Answers
from NLP import mapa
#import subfunctions
from telebot import types
import config
from Command_package import Commands
import os
import sys
from requests.exceptions import ConnectionError, ReadTimeout
import time
import flask
#import requests
import logging
from bot import *


# ______________________________________________________________________________
API_TOKEN = '5301739662:AAGWfetEsSQNUUiykxU9WL0pL5D2-9imlec'
APP_HOST = '127.0.0.1'
APP_PORT = '9000'


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
boto = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    if(flask.request.headers.get('content-type') == 'application/json'):
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        boto.process_new_updates([update])
        return ''
    else:
        boto.flask.abort(403)
