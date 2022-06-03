import NLP
#import pyTelegramBotAPI
import RPA
import psycopg2

def commandsdesition(boto, message, reply_markup, tstr):
    global command_flag
    preinpt = message.text.split('->')
    inpt = preinpt[0].split(' ')
    print(inpt)
    if(NLP.NLP.preprocess_text(inpt[1]) == 'атаковать' or
       NLP.NLP.preprocess_text(inpt[1]) == 'фас' or 
       NLP.NLP.preprocess_text(inpt[1]) == 'пизданутьimport rpa as r'):
        fas(boto, message, reply_markup)
        command_flag = 0
    elif NLP.NLP.preprocess_text(inpt[1]) == 'находить':
        RPA.founder(boto, message, reply_markup, NLP.NLP.preprocess_text(preinpt[1]))
        command_flag = 0

    else:

        boto.send_message(message.chat.id, "Команда",
                          parse_mode='html', reply_markup=reply_markup)


def fas(boto, message, reply_markup):

    inpt = message.text.split(' ')

    boto.send_message(message.chat.id, inpt[2] + " - пидор.",
                      parse_mode='html', reply_markup=reply_markup)
