import bot
from Bot_package import Botoevaluaters

@bot.boto.message_handler(commands=['hievaluate'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Botoevaluaters.Binaryevaluate()

        bt.hievaluate()
        bot.boto.send_photo(message.chat.id,
                            photo=open('./models/binary/results_training/resultstraining_binary.png', 'rb'))
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['quevaluate'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Botoevaluaters.Binaryevaluate()

        bt.quevaluate()
        bot.boto.send_photo(message.chat.id,
                            photo=open('./models/binary/results_training/resultstraining_binary.png', 'rb'))
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['thevaluate'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Botoevaluaters.Binaryevaluate()

        bt.thevaluate()
        bot.boto.send_photo(message.chat.id,
                            photo=open('./models/binary/results_training/resultstraining_binary.png', 'rb'))
    else:
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')

@bot.boto.message_handler(commands=['commandevaluate'])
def get_user_text(message):
    if (message.chat.username == 'Polyakov_Max'):
        bt = Botoevaluaters.Binaryevaluate()
        bt.commandevaluate()
        bot.boto.send_photo(message.chat.id,
                            photo=open('./models/binary/results_training/resultstraining_binary.png', 'rb'))
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
