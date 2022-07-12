import bot

class Train:
    def __init__(self):
        pass
    def hitrain(self):
        pass
    def qutrain(self):
        pass
    def thtrain(self):
        pass
    def commandtrain(self):
        pass
    def hi_th_commandtrain(self):
        pass
    def multyclasstrain(self):
        pass

class Binarytrain(Train):
    def __init__(self):
        pass

    def hitrain(self):
        filemodel = './models/binary/himodel.h5'
        filetokenizer = './tokenizers/binary/hitokenizer.pickle'
        datasetfile = 'SELECT * FROM hiset'
        recognizeddata = 'SELECT * FROM recognized_hi'
        trainer = bot.Models.Binary(filemodel, filetokenizer,
                                datasetfile, recognizeddata)
        trainer.train('hi', 'train')

    def qutrain(self):
        filemodel = './models/binary/qumodel.h5'
        filetokenizer = './tokenizers/binary/qutokenizer.pickle'
        datasetfile = 'SELECT * FROM questionset'
        recognizeddata = 'SELECT * FROM recognized_qu'
        trainer = bot.Models.Binary(filemodel, filetokenizer,
                                datasetfile, recognizeddata)
        trainer.train('question', 'train')

    def thtrain(self):
        filemodel = './models/binary/thmodel.h5'
        filetokenizer = './tokenizers/binary/thtokenizer.pickle'
        datasetfile = 'SELECT * FROM thanksset'
        recognizeddata = 'SELECT * FROM recognized_th'
        trainer = bot.Models.Binary(filemodel, filetokenizer,
                                datasetfile, recognizeddata)
        trainer.train('thanks', 'train')

    def commandtrain(self):
        filemodel = './models/binary/commandmodel.h5'
        filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
        datasetfile = 'SELECT * FROM commandset'
        recognizeddata = 'SELECT * FROM recognized_command'
        trainer = bot.Models.Binary(filemodel, filetokenizer,
                                datasetfile, recognizeddata)
        trainer.train('command', 'train')

class Multytrain(Train):
    def __init__(self):
        pass

    def hi_th_commandtrain(self):
        trainer = bot.Models.Multy('./models/multy/hi_th_commandmodel.h5',
                                   './tokenizers/multy/hi_th_commandtokenizer.pickle',
                                   'SELECT * FROM hi_th_command',
                                   'SELECT * FROM recognized_hi_th_command')

        trainer.train('hi_th_command', 4, 'train')
    def multyclasstrain(self):
        trainer = bot.Models.Multy('./models/multy/multyclassmodel.h5',
                                   './tokenizers/multy/multyclasstokenizer.pickle',
                                   'SELECT * FROM multyclasesset',
                                   'SELECT * FROM recognized_multyclass')
        trainer.train('questionclass', 3, 'train')

class NonNeuroTrain(Train):
    def hitrain(self):
        filemodel = './models/binary/himodel.pickle'
        filetokenizer = './tokenizers/binary/hivec.pickle'
        datasetfile = 'SELECT * FROM hiset'
        recognizeddata = 'SELECT * FROM recognized_hi'
        trainer = bot.Models.NonNeuro(filemodel,filetokenizer,datasetfile,recognizeddata)
        trainer.train('hi', 'train')

    def thtrain(self):
        filemodel = './models/binary/thmodel.pickle'
        filetokenizer = './tokenizers/binary/thvec.pickle'
        datasetfile = 'SELECT * FROM thanksset'
        recognizeddata = 'SELECT * FROM recognized_th'

        trainer = bot.Models.NonNeuro(filemodel,filetokenizer,datasetfile,recognizeddata)

        trainer.train('thanks', 'train')

    def multyclasstrain(self):

        filemodel = './models/binary/multyclassmodel.pickle'
        filetokenizer = './tokenizers/binary/multvec.pickle'
        datasetfile = 'SELECT * FROM multyclasesset'
        recognizeddata = 'SELECT * FROM recognized_multyclass'

        trainer = bot.Models.NonNeuro(filemodel,filetokenizer,datasetfile,recognizeddata)

        trainer.train('questionclass', 'train')
