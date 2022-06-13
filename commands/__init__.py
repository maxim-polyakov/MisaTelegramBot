import NLP
from NLP import TextPreprocessers
#import pyTelegramBotAPI
from RPA_module import Founders
import psycopg2

def commandsdesition(boto, message, reply_markup, tstr):
    global command_flag
    pr = TextPreprocessers.CommonPreprocessing()
    preinpt = message.text.split('->')
    inpt = preinpt[0].split(' ')
    print(inpt)
    if(pr.preprocess_text(inpt[1]) == 'атаковать' or
       pr.preprocess_text(inpt[1]) == 'фас' or 
       pr.preprocess_text(inpt[1]) == 'пиздануть'):
        fas(boto, message, reply_markup)
        command_flag = 1
    elif pr.preprocess_text(inpt[1]) == 'находить':
        
        print(preinpt[1])
        f = Founders.WikiFounder()
        f.find(boto, message, reply_markup, pr.preprocess_text(preinpt[1]))
        
        command_flag = 1

    else:

        boto.send_message(message.chat.id, "Команда",
                          parse_mode='html', reply_markup=reply_markup)
        command_flag = 1

    return command_flag

def fas(boto, message, reply_markup):

    inpt = message.text.split(' ')

    boto.send_message(message.chat.id, inpt[2] + " - пидор.",
                      parse_mode='html', reply_markup=reply_markup)
