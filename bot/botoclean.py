import bot
#import pyTelegramBotAPI
from NLP import DataCleaners

@bot.boto.message_handler(commands=['multyclean'])
def get_user_text(message):
    cl = DataCleaners.CommonCleaner()
    strr = message.text.replace('/multyclean ','')

    cl.clean('./datasets/' + strr, 'questionclass')
    bot.boto.send_message(message.chat.id, strr + " is cleaned", parse_mode='html')


@bot.boto.message_handler(commands=['clean'])
def get_user_text(message):
    cl = DataCleaners.CommonCleaner()
    strr = message.text.replace('/multyclean ','')
    strrr = strr.split(strr)
    cl.clean('./datasets/' + strrr[0], strrr[1])
    bot.boto.send_message(message.chat.id, " is cleaned", parse_mode='html')

#______________________________________________________________________________