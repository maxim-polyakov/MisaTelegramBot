import core
import messagemonitor
import bototrain
#import pyTelegramBotAPI
#______________________________________________________________________________



#______________________________________________________________________________


@core.boto.message_handler(commands=['multyclean'])
def get_user_text(message):
    core.NLP.DataCleaner('./datasets/multyclasesset.xlsx', 'questionclass')
    core.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@core.boto.message_handler(commands=['hiclean'])
def get_user_text(message):
    core.NLP.DataCleaner('./datasets/dataset.xlsx', 'hi')
    core.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@core.boto.message_handler(commands=['quclean'])
def get_user_text(message):
    core.NLP.QuestionsetCleaner('./datasets/questionset.xlsx')
    core.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@core.boto.message_handler(commands=['thclean'])
def get_user_text(message):
    core.NLP.DataCleaner('./datasets/thanksset.xlsx', 'thanks')
    core.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@core.boto.message_handler(commands=['commandclean'])
def get_user_text(message):

    core.NLP.CommandsetCleaner('./datasets/commandset.xlsx')
    core.boto.send_message(message.chat.id, "cleaned", parse_mode='html')
#______________________________________________________________________________




