import bot
#import pyTelegramBotAPI
from NLP import DataCleaners

@bot.boto.message_handler(commands=['multyclean'])
def get_user_text(message):
    cl = DataCleaners.CommonCleaner()
    
    cl.clean('./datasets/multyclasesset.xlsx', 'questionclass')
    bot.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@bot.boto.message_handler(commands=['hiclean'])
def get_user_text(message):
    cl = DataCleaners.CommonCleaner()
    
    cl.clean('./datasets/dataset.xlsx', 'hi')
    bot.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@bot.boto.message_handler(commands=['quclean'])
def get_user_text(message):
    cl = DataCleaners.QuestionCleaner()
    cl.clean('./datasets/questionset.xlsx')
    bot.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@bot.boto.message_handler(commands=['thclean'])
def get_user_text(message):
    cl = DataCleaners.CommonCleaner()
    cl.clean('./datasets/thanksset.xlsx', 'thanks')
    bot.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@bot.boto.message_handler(commands=['commandclean'])
def get_user_text(message):
    cl = DataCleaners.CommandsetCleaner()
    cl.clean('./datasets/commandset.xlsx')
    bot.boto.send_message(message.chat.id, "cleaned", parse_mode='html')
#______________________________________________________________________________




@bot.boto.message_handler(commands=['weatherclean'])
def get_user_text(message):
    cl = DataCleaners.CommonCleaner()
    
    cl.clean('./datasets/weather.xlsx', 'questionclass')
    bot.boto.send_message(message.chat.id, "cleaned", parse_mode='html')