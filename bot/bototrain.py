import bot
from Bot_package import Bototrainers
from Bot_package import Botoevaluaters
#import messagemonitor

# ______________________________________________________________________________

@bot.boto.message_handler(commands=['hitrain'])
def get_user_text(message):
    bt = Bototrainers.Binarytrain()
    bt.hitrain()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')


@bot.boto.message_handler(commands=['qutrain'])
def get_user_text(message):
    bt = Bototrainers.Binarytrain()
    bt.qutrain()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')


@bot.boto.message_handler(commands=['thtrain'])
def get_user_text(message):

    bt = Bototrainers.Binarytrain()
    bt.thtrain()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')


@bot.boto.message_handler(commands=['commandtrain'])
def get_user_text(message):
    bt = Bototrainers.Binarytrain()

    bt.commandtrain()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
# ______________________________________________________________________________


@bot.boto.message_handler(commands=['hievaluate'])
def get_user_text(message):
    bt = Botoevaluaters.Binaryevaluate()

    bt.hievaluate()


@bot.boto.message_handler(commands=['quevaluate'])
def get_user_text(message):
    bt = Bototrainers.Binarytrain()

    bt.quevaluate()


@bot.boto.message_handler(commands=['thevaluate'])
def get_user_text(message):
    bt = Botoevaluaters.Binaryevaluate()

    bt.thevaluate()


@bot.boto.message_handler(commands=['commandevaluate'])
def get_user_text(message):
    bt = Botoevaluaters.Binaryevaluate()

    bt.commandevaluate()


@bot.boto.message_handler(commands=['multyclasstrain'])
def get_user_text(message):

    mt = Bototrainers.Multytrain()

    mt.multyclasstrain()


    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')

@bot.boto.message_handler(commands=['hi_th_commandtrain'])
def get_user_text(message):

    mt = Bototrainers.Multytrain()

    mt.hi_th_commandtrain()

    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')

@bot.boto.message_handler(commands=['NonNeurotrain'])
def get_user_text(message):

    mt = Bototrainers.NonNeuroTrain()

    mt.hitrain()
    mt.thtrain()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')


