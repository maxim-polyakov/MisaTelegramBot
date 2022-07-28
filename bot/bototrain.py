import bot
from Bot_package import Bototrainers


@bot.boto.message_handler(commands=['hitrain'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Bototrainers.Binarytrain()
        bt.hitrain()
        bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
        bot.boto.send_photo(message.chat.id,
                            photo=open('./models/binary/results_training/resultstraining_binary.png', 'rb'))
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['qutrain'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Bototrainers.Binarytrain()
        bt.qutrain()
        bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
        bot.boto.send_photo(message.chat.id,
                            photo=open('./models/binary/results_training/resultstraining_binary.png', 'rb'))
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['thtrain'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Bototrainers.Binarytrain()
        bt.thtrain()
        bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
        bot.boto.send_photo(message.chat.id,
                            photo=open('./models/binary/results_training/resultstraining_binary.png', 'rb'))
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['commandtrain'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Bototrainers.Binarytrain()
        bt.commandtrain()
        bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
        bot.boto.send_photo(message.chat.id,
                            photo=open('./models/binary/results_training/resultstraining_binary.png', 'rb'))
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['multyclasstrain'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        mt = Bototrainers.Multytrain()
        mt.multyclasstrain()
        bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['hi_th_commandtrain'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        mt = Bototrainers.Multytrain()
        mt.hi_th_commandtrain()
        bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['NonNeurotrain'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        mt = Bototrainers.NonNeuroTrain()
        mt.hitrain()
        mt.thtrain()
        mt.multyclasstrain()
        bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['emotionstrain'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        mt = Bototrainers.NonNeuroTrain()
        mb = Bototrainers.Multytrain()
        mb.emotionstrain()
        bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')




