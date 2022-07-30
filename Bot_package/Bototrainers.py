import Bot_package

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
    def emotionstrain(self):
        pass

class Binarytrain(Train):
    def __init__(self):
        pass

    def hitrain(self):
        filemodel = './models/binary/himodel.h5'
        filetokenizer = './tokenizers/binary/hitokenizer.pickle'
        datasetfile = 'SELECT * FROM hiset'
        recognizeddata = 'SELECT * FROM recognized_hiset'
        trainer = Bot_package.Models.BinaryLSTM(filemodel, filetokenizer,
                                        datasetfile, recognizeddata)
        trainer.train('hi', 'train')

    def qutrain(self):
        filemodel = './models/binary/qumodel.h5'
        filetokenizer = './tokenizers/binary/qutokenizer.pickle'
        datasetfile = 'SELECT * FROM questionset'
        recognizeddata = 'SELECT * FROM recognized_questionset'
        trainer = Bot_package.Models.BinaryLSTM(filemodel, filetokenizer,
                                        datasetfile, recognizeddata)
        trainer.train('question', 'train')

    def thtrain(self):
        filemodel = './models/binary/thmodel.h5'
        filetokenizer = './tokenizers/binary/thtokenizer.pickle'
        datasetfile = 'SELECT * FROM thanksset'
        recognizeddata = 'SELECT * FROM recognized_thanksset'
        trainer = Bot_package.Models.BinaryLSTM(filemodel, filetokenizer,
                                        datasetfile, recognizeddata)
        trainer.train('thanks', 'train')

    def commandtrain(self):
        filemodel = './models/binary/commandmodel.h5'
        filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
        datasetfile = 'SELECT * FROM commandset'
        recognizeddata = 'SELECT * FROM recognized_commandset'
        trainer = Bot_package.Models.BinaryLSTM(filemodel, filetokenizer,
                                        datasetfile, recognizeddata)
        trainer.train('command', 'train')

class Multytrain(Train):
    def __init__(self):
        pass

    def hi_th_commandtrain(self):
        trainer = Bot_package.Models.MultyLSTM('./models/multy/hi_th_commandmodel.h5',
                                   './tokenizers/multy/hi_th_commandtokenizer.pickle',
                                   'SELECT * FROM hi_th_command',
                                   'SELECT * FROM recognized_hi_th_command')

        trainer.train('hi_th_command', 4, 'train')
    def multyclasstrain(self):
        trainer = Bot_package.Models.MultyLSTM('./models/multy/multyclassmodel.h5',
                                   './tokenizers/multy/multyclasstokenizer.pickle',
                                   'SELECT * FROM multyclasesset',
                                   'SELECT * FROM recognized_multyclasesset')
        trainer.train('questionclass', 3, 'train')

    def emotionstrain(self):
        trainer = Bot_package.Models.MultyLSTM('./models/multy/emotionsmodel.h5',
                                   './tokenizers/multy/emotionstokenizer.pickle',
                                   'SELECT * FROM emotionstrain',
                                   'SELECT * FROM recognized_emotionstrain')
        trainer.train('emotionid', 7, 'train')

class NonNeuroTrain(Train):
    def hitrain(self):
        filemodel = './models/binary/himodel.pickle'
        filetokenizer = './tokenizers/binary/hivec.pickle'
        datasetfile = 'SELECT * FROM hiset'
        recognizeddata = 'SELECT * FROM recognized_hiset'
        trainer = Bot_package.Models.NonNeuro(filemodel,filetokenizer,datasetfile,recognizeddata)
        trainer.train('hi', 'train')

    def thtrain(self):
        filemodel = './models/binary/thmodel.pickle'
        filetokenizer = './tokenizers/binary/thvec.pickle'
        datasetfile = 'SELECT * FROM thanksset'
        recognizeddata = 'SELECT * FROM recognized_thhanksset'

        trainer = Bot_package.Models.NonNeuro(filemodel,filetokenizer,datasetfile,recognizeddata)

        trainer.train('thanks', 'train')

    def multyclasstrain(self):

        filemodel = './models/binary/multyclassmodel.pickle'
        filetokenizer = './tokenizers/binary/multvec.pickle'
        datasetfile = 'SELECT * FROM multyclasesset'
        recognizeddata = 'SELECT * FROM recognized_multyclasesset'

        trainer = Bot_package.Models.NonNeuro(filemodel,filetokenizer,datasetfile,recognizeddata)

        trainer.train('questionclass', 'train')

    def emotionstrain(self):
        filemodel = './models/binary/emotionsmodel.pickle'
        filetokenizer = './tokenizers/binary/emotionsvec.pickle'
        datasetfile = 'SELECT * FROM emotionstrain'
        recognizeddata = 'SELECT * FROM recognized_emotionstrain'


        trainer = Bot_package.Models.NonNeuro(filemodel,filetokenizer,datasetfile,recognizeddata)

        trainer.train('questionclass', 'train')
