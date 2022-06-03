import bot
#import messagemonitor

#______________________________________________________________________________


def hitrain():
    filemodel = './models/binary/himodel.h5'
    filetokenizer = './tokenizers/binary/hitokenizer.pickle'
    datasetfile = 'SELECT * FROM hiset'
    recognizeddata = 'SELECT * FROM recognized_hi'
    trainer = bot.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('hi','train')


def hievaluate():
    filemodel = './models/binary/himodel.h5'
    filetokenizer = './tokenizers/binary/hitokenizer.pickle'
    datasetfile = 'SELECT * FROM hiset'
    recognizeddata = 'SELECT * FROM recognized_hi'
    trainer = bot.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('hi','evaluate')


def qutrain():
    filemodel = './models/binary/qumodel.h5'
    filetokenizer = './tokenizers/binary/qutokenizer.pickle'
    datasetfile = 'SELECT * FROM questionset'
    recognizeddata = 'SELECT * FROM recognized_qu'
    trainer = bot.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('question','train')


def quevaluate():
    filemodel = './models/binary/qumodel.h5'
    filetokenizer = './tokenizers/binary/qutokenizer.pickle'
    datasetfile = 'SELECT * FROM questionset'
    recognizeddata = 'SELECT * FROM recognized_qu'
    trainer = bot.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('question','evaluate')


def thtrain():
    filemodel = './models/binary/thmodel.h5'
    filetokenizer = './tokenizers/binary/thtokenizer.pickle'
    datasetfile = 'SELECT * FROM thanksset'
    recognizeddata = 'SELECT * FROM recognized_th'
    trainer = bot.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('thanks','train')


def thevaluate():
    filemodel = './models/binary/qumodel.h5'
    filetokenizer = './tokenizers/binary/thtokenizer.pickle'
    datasetfile = 'SELECT * FROM thanksset'
    recognizeddata = 'SELECT * FROM recognized_th'
    trainer = bot.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('thanks','evaluate')


def commandtrain():
    filemodel = './models/binary/commandmodel.h5'
    filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
    datasetfile = 'SELECT * FROM commandset'
    recognizeddata = 'SELECT * FROM recognized_command'
    trainer = bot.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('command','train')


def commandevaluate():
    filemodel = './models/binary/commandmodel.h5'
    filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
    datasetfile = 'SELECT * FROM commandset'
    recognizeddata = 'SELECT * FROM recognized_command'
    trainer = bot.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('command','evaluate')
#______________________________________________________________________________


@bot.boto.message_handler(commands=['hitrain'])
def get_user_text(message):

    hitrain()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')


@bot.boto.message_handler(commands=['qutrain'])
def get_user_text(message):

    qutrain()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')


@bot.boto.message_handler(commands=['thtrain'])
def get_user_text(message):

    thtrain()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')


@bot.boto.message_handler(commands=['commandtrain'])
def get_user_text(message):

    commandtrain()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')
#______________________________________________________________________________


@bot.boto.message_handler(commands=['hievaluate'])
def get_user_text(message):

    hievaluate()


@bot.boto.message_handler(commands=['quevaluate'])
def get_user_text(message):

    quevaluate()
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')


@bot.boto.message_handler(commands=['thevaluate'])
def get_user_text(message):

    thevaluate()


@bot.boto.message_handler(commands=['commandevaluate'])
def get_user_text(message):

    commandevaluate()
    
@bot.boto.message_handler(commands=['multyclasstrain'])
def get_user_text(message):

    trainer = bot.NLP.Multy()
    trainer.multyclasstrain('train')
    bot.boto.send_message(message.chat.id, "trained", parse_mode='html')