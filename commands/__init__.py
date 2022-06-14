import NLP
from NLP import TextPreprocessers
#import pyTelegramBotAPI
from RPA_module import Founders
from RPA_module import Calculators
import psycopg2

def commandsdesition(boto, message, tstr):
    global command_flag
    pred = TextPreprocessers.Preprocessing()
    pr = TextPreprocessers.CommonPreprocessing()
    cpr = TextPreprocessers.CommandPreprocessing()
    preinpt = message.text.split('->')

    strr = pred.preprocess_text(preinpt[0])
    inpt = strr.split(' ')
    print(inpt)
    if(pr.preprocess_text(inpt[1]) == 'атаковать' or
       pr.preprocess_text(inpt[1]) == 'фас' or 
       pr.preprocess_text(inpt[1]) == 'пиздануть'):
        fas(boto, message)
        command_flag = 1
    elif pr.preprocess_text(inpt[1]) == 'находить':
        
        print(preinpt[1])
        f = Founders.WikiFounder()
        f.find(boto, message, pr.preprocess_text(preinpt[1]))
        
        command_flag = 1
    elif pr.preprocess_text(inpt[1]) == 'поссчитать' or pr.preprocess_text(inpt[1]) == 'находить':
        if pr.preprocess_text(inpt[2]) == 'производная':
            c = Calculators.WolframCalculator()
            print(inpt[3])
            c.deravative(boto, message, inpt[3])
        
    else:

        boto.send_message(message.chat.id, "Команда",
                          parse_mode='html')
        command_flag = 1


def fas(boto, message):

    inpt = message.text.split(' ')

    boto.send_message(message.chat.id, inpt[2] + " - пидор.",
                      parse_mode='html')
