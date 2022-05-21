import NLP
import telebot

def commandsdesition(boto, message, reply_markup, tstr):
    inpt = message.text.split(' ')
    print(inpt)
    if(NLP.libraries.preprocess_text(inpt[1]) == 'атаковать' or NLP.libraries.preprocess_text(inpt[1]) == 'фас'):
        fas(boto, message, reply_markup)
    else:
        boto.send_message(message.chat.id, "Команда",
                          parse_mode='html', reply_markup=reply_markup)
    






def fas(boto, message, reply_markup):
    

    inpt = message.text.split(' ')
    
    boto.send_message(message.chat.id, inpt[2] + " - пидор.",
                      parse_mode='html', reply_markup=reply_markup)
