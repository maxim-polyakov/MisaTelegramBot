import NLP
import telebot
import RPA


def commandsdesition(boto, message, reply_markup, tstr):
    inpt = message.text.split(' ')
    print(inpt)
    if(NLP.libraries.preprocess_text(inpt[1]) == 'атаковать' or
       NLP.libraries.preprocess_text(inpt[1]) == 'фас' or 
       NLP.libraries.preprocess_text(inpt[1]) == 'пизданутьimport rpa as r'):
        fas(boto, message, reply_markup)
    elif NLP.libraries.preprocess_text(inpt[1]) == 'находить':
        RPA.founder(boto, message, reply_markup)
    else:
        boto.send_message(message.chat.id, "Команда",
                          parse_mode='html', reply_markup=reply_markup)


def fas(boto, message, reply_markup):

    inpt = message.text.split(' ')

    boto.send_message(message.chat.id, inpt[2] + " - пидор.",
                      parse_mode='html', reply_markup=reply_markup)
