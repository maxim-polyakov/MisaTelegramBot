import bot
#import pyTelegramBotAPI
from Bot_package import DataCleaners


@bot.boto.message_handler(commands=['multyclean'])
def get_user_text(message):
    cl = DataCleaners.CommonCleaner()
    strr = message.text.replace('/multyclean ','')
    strrr = strr.split(' ')
    cl.clean('./datasets/' + strrr[0], strrr[1])
    bot.boto.send_message(message.chat.id, strr + " is cleaned", parse_mode='html')


@bot.boto.message_handler(commands=['clean'])
def get_user_text(message):
    cl = DataCleaners.CommonCleaner()
    strr = message.text.replace('/clean ','')
    strrr = strr.split(' ')
    cl.clean('./datasets/' + strrr[0], strrr[1])
    bot.boto.send_message(message.chat.id, " is cleaned", parse_mode='html')
    
@bot.boto.message_handler(commands=['cleancsv'])
def get_user_text(message):
    cl = DataCleaners.CommonCleaner("csv")
    strr = message.text.replace('/cleancsv ','')
    print(strr)
    strrr = strr.split(' ')
    print('strrr[0] = ',strrr)
    cl.clean('./datasets/' + strrr[0], strrr[1])
    bot.boto.send_message(message.chat.id, " is cleaned", parse_mode='html')

#______________________________________________________________________________