import NLP
import telebot

def commandsdesition(boto, message, reply_markup, tstr):
    if(NLP.libraries.preprocess_text(tstr) == 'фас'):
        fas(boto, message, reply_markup)
    else:
        boto.send_message(message.chat.id, "Команда",
                          parse_mode='html', reply_markup=reply_markup)
    






def fas(boto, message, reply_markup):
    

    
    
    boto.send_message(message.chat.id, "Атака",
                      parse_mode='html', reply_markup=reply_markup)
