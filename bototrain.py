import core
#import messagemonitor

#______________________________________________________________________________


def hitrain():
    filemodel = './models/binary/himodel.h5'
    filetokenizer = './tokenizers/binary/hitokenizer.pickle'
    datasetfile = 'SELECT * FROM hiset'
    recognizeddata = 'SELECT * FROM recognized_hi'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('hi','train')


def hievaluate():
    filemodel = './models/binary/himodel.h5'
    filetokenizer = './tokenizers/binary/hitokenizer.pickle'
    datasetfile = 'SELECT * FROM hiset'
    recognizeddata = 'SELECT * FROM recognized_hi'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('hi','evaluate')


def qutrain():
    filemodel = './models/binary/qumodel.h5'
    filetokenizer = './tokenizers/binary/qutokenizer.pickle'
    datasetfile = 'SELECT * FROM questionset'
    recognizeddata = 'SELECT * FROM recognized_qu'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('question','train')


def quevaluate():
    filemodel = './models/binary/qumodel.h5'
    filetokenizer = './tokenizers/binary/qutokenizer.pickle'
    datasetfile = 'SELECT * FROM questionset'
    recognizeddata = 'SELECT * FROM recognized_qu'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('question','evaluate')


def thtrain():
    filemodel = './models/binary/thmodel.h5'
    filetokenizer = './tokenizers/binary/thtokenizer.pickle'
    datasetfile = 'SELECT * FROM thanksset'
    recognizeddata = 'SELECT * FROM recognized_th'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('thanks','train')


def thevaluate():
    filemodel = './models/binary/qumodel.h5'
    filetokenizer = './tokenizers/binary/thtokenizer.pickle'
    datasetfile = 'SELECT * FROM thanksset'
    recognizeddata = 'SELECT * FROM recognized_th'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('thanks','evaluate')


def commandtrain():
    filemodel = './models/binary/commandmodel.h5'
    filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
    datasetfile = 'SELECT * FROM commandset'
    recognizeddata = 'SELECT * FROM recognized_command'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('command','train')


def commandevaluate():
    filemodel = './models/binary/commandmodel.h5'
    filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
    datasetfile = 'SELECT * FROM commandset'
    recognizeddata = 'SELECT * FROM recognized_command'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('command','evaluate')
#______________________________________________________________________________


@core.boto.message_handler(commands=['hitrain'])
def get_user_text(message):

    hitrain()
    core.boto.send_message(message.chat.id, "trained", parse_mode='html')


@core.boto.message_handler(commands=['qutrain'])
def get_user_text(message):

    qutrain()
    core.boto.send_message(message.chat.id, "trained", parse_mode='html')


@core.boto.message_handler(commands=['thtrain'])
def get_user_text(message):

    thtrain()
    core.boto.send_message(message.chat.id, "trained", parse_mode='html')


@core.boto.message_handler(commands=['commandtrain'])
def get_user_text(message):

    commandtrain()
    core.boto.send_message(message.chat.id, "trained", parse_mode='html')
#______________________________________________________________________________


@core.boto.message_handler(commands=['hievaluate'])
def get_user_text(message):

    hievaluate()


@core.boto.message_handler(commands=['quevaluate'])
def get_user_text(message):

    quevaluate()
    core.boto.send_message(message.chat.id, "trained", parse_mode='html')


@core.boto.message_handler(commands=['thevaluate'])
def get_user_text(message):

    thevaluate()


@core.boto.message_handler(commands=['commandevaluate'])
def get_user_text(message):

    commandevaluate()
    
@core.boto.message_handler(commands=['multyclasstrain'])
def get_user_text(message):

    trainer = core.NLP.Multy()
    trainer.multyclasstrain('train')
    core.boto.send_message(message.chat.id, "trained", parse_mode='html')