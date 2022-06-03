import bot
#import pyTelegramBotAPI


@bot.boto.message_handler(commands=['multyclean'])
def get_user_text(message):
    bot.NLP.DataCleaner('./datasets/multyclasesset.xlsx', 'questionclass')
    bot.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@bot.boto.message_handler(commands=['hiclean'])
def get_user_text(message):
    bot.NLP.DataCleaner('./datasets/dataset.xlsx', 'hi')
    bot.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@bot.boto.message_handler(commands=['quclean'])
def get_user_text(message):
    bot.NLP.QuestionsetCleaner('./datasets/questionset.xlsx')
    bot.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@bot.boto.message_handler(commands=['thclean'])
def get_user_text(message):
    bot.NLP.DataCleaner('./datasets/thanksset.xlsx', 'thanks')
    bot.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@bot.boto.message_handler(commands=['commandclean'])
def get_user_text(message):

    bot.NLP.CommandsetCleaner('./datasets/commandset.xlsx')
    bot.boto.send_message(message.chat.id, "cleaned", parse_mode='html')
#______________________________________________________________________________




@bot.boto.message_handler(commands=['weatherclean'])
def get_user_text(message):
    print('here')
    bot.NLP.DataCleaner('./datasets/weather.xlsx', 'questionclass')
    bot.boto.send_message(message.chat.id, "cleaned", parse_mode='html')