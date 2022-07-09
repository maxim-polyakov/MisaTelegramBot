import bot

class Evaluate:
    def __init__(self):
        pass
    def hievaluate(self):
        pass
    def quevaluate(self):
        pass
    def thevaluate(self):
        pass
    def commandevaluate(self):
        pass

class Binaryevaluate(Evaluate):
    def __init__(self):
        pass
    def hievaluate(self):
        filemodel = './models/binary/himodel.h5'
        filetokenizer = './tokenizers/binary/hitokenizer.pickle'
        datasetfile = 'SELECT * FROM hiset'
        recognizeddata = 'SELECT * FROM recognized_hi'
        trainer = bot.Models.Binary(filemodel, filetokenizer,
                                datasetfile, recognizeddata)
        trainer.train('hi', 'evaluate')

    def quevaluate(self):
        filemodel = './models/binary/qumodel.h5'
        filetokenizer = './tokenizers/binary/qutokenizer.pickle'
        datasetfile = 'SELECT * FROM questionset'
        recognizeddata = 'SELECT * FROM recognized_qu'
        trainer = bot.Models.Binary(filemodel, filetokenizer,
                                datasetfile, recognizeddata)
        trainer.train('question', 'evaluate')

    def thevaluate(self):
        filemodel = './models/binary/qumodel.h5'
        filetokenizer = './tokenizers/binary/thtokenizer.pickle'
        datasetfile = 'SELECT * FROM thanksset'
        recognizeddata = 'SELECT * FROM recognized_th'
        trainer = bot.Models.Binary(filemodel, filetokenizer,
                                datasetfile, recognizeddata)
        trainer.train('thanks', 'evaluate')

    def commandevaluate(self):
        filemodel = './models/binary/commandmodel.h5'
        filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
        datasetfile = 'SELECT * FROM commandset'
        recognizeddata = 'SELECT * FROM recognized_command'
        trainer = bot.Models.Binary(filemodel, filetokenizer,
                                datasetfile, recognizeddata)
        trainer.train('command', 'evaluate')