import bot
from Bot_package import Bototrain
from Bot_package import Botoevaluate
#import messagemonitor

# ______________________________________________________________________________

@bot.boto.message_handler(commands=['hitrain'])
def get_user_text(message):
    bt = Bototrain.Binarytrain()
    bt.hitrain()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')


@bot.boto.message_handler(commands=['qutrain'])
def get_user_text(message):
    bt = Bototrain.Binarytrain()
    bt.qutrain()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')


@bot.boto.message_handler(commands=['thtrain'])
def get_user_text(message):

    bt = Bototrain.Binarytrain()
    bt.thtrain()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')


@bot.boto.message_handler(commands=['commandtrain'])
def get_user_text(message):
    bt = Bototrain.Binarytrain()

    bt.commandtrain()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
# ______________________________________________________________________________


@bot.boto.message_handler(commands=['hievaluate'])
def get_user_text(message):
    bt = Botoevaluate.Binaryevaluate()

    bt.hievaluate()


@bot.boto.message_handler(commands=['quevaluate'])
def get_user_text(message):
    bt = Bototrain.Binarytrain()

    bt.quevaluate()


@bot.boto.message_handler(commands=['thevaluate'])
def get_user_text(message):
    bt = Botoevaluate.Binaryevaluate()

    bt.thevaluate()


@bot.boto.message_handler(commands=['commandevaluate'])
def get_user_text(message):
    bt = Botoevaluate.Binaryevaluate()

    bt.commandevaluate()


@bot.boto.message_handler(commands=['multyclasstrain'])
def get_user_text(message):

    mt = Bototrain.Multytrain()

    mt.multyclasstrain()


    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')

@bot.boto.message_handler(commands=['hi_th_commandtrain'])
def get_user_text(message):

    mt = Bototrain.Multytrain()

    mt.hi_th_commandtrain()

    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
