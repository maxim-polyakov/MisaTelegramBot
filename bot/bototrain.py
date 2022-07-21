import bot
from Bot_package import Bototrainers
from Bot_package import Botoevaluaters
#import messagemonitor

# ______________________________________________________________________________

@bot.boto.message_handler(commands=['hitrain'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Bototrainers.Binarytrain()
        bt.hitrain()
        bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['qutrain'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Bototrainers.Binarytrain()
        bt.qutrain()
        bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['thtrain'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Bototrainers.Binarytrain()
        bt.thtrain()
        bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['commandtrain'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Bototrainers.Binarytrain()
        bt.commandtrain()
        bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')
# ______________________________________________________________________________


@bot.boto.message_handler(commands=['hievaluate'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Botoevaluaters.Binaryevaluate()

        bt.hievaluate()
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['quevaluate'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Bototrainers.Binarytrain()

        bt.quevaluate()
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['thevaluate'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Botoevaluaters.Binaryevaluate()

        bt.thevaluate()
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['commandevaluate'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Botoevaluaters.Binaryevaluate()
        bt.commandevaluate()
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

@bot.boto.message_handler(commands=['emotionsevaluate'])
def get_user_text(message):
    if(message.chat.username == 'Polyakov_Max'):
        # mt = Bototrainers.NonNeuroT()
        mb = Botoevaluaters.Multyevaluate()
        mb.emotionsevaluate()
        bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['checkname'])
def get_user_text(message):
    print(message)
    bot.boto.send_message(message.chat.id, message.chat.username, parse_mode='html')




