import Bot_package

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
    def hi_th_commandevaluate(self):
        pass
    def multyclassevaluate(self):
        pass
    def emotionsevaluate(self):
        pass

class Binaryevaluate(Evaluate):
    def __init__(self):
        pass
    def hievaluate(self):
        filemodel = './models/binary/himodel.h5'
        filetokenizer = './tokenizers/binary/hitokenizer.pickle'
        datasetfile = 'SELECT * FROM hiset'
        recognizeddata = 'SELECT * FROM recognized_hiset'
        trainer =Bot_package.Models.BinaryLSTM(filemodel, filetokenizer,
                                        datasetfile, recognizeddata)
        trainer.train('hi', 'evaluate')

    def quevaluate(self):
        filemodel = './models/binary/qumodel.h5'
        filetokenizer = './tokenizers/binary/qutokenizer.pickle'
        datasetfile = 'SELECT * FROM questionset'
        recognizeddata = 'SELECT * FROM recognized_questionset'
        trainer = Bot_package.Models.BinaryLSTM(filemodel, filetokenizer,
                                        datasetfile, recognizeddata)
        trainer.train('question', 'evaluate')

    def thevaluate(self):
        filemodel = './models/binary/qumodel.h5'
        filetokenizer = './tokenizers/binary/thtokenizer.pickle'
        datasetfile = 'SELECT * FROM thanksset'
        recognizeddata = 'SELECT * FROM recognized_thanksset'
        trainer = Bot_package.Models.BinaryLSTM(filemodel, filetokenizer,
                                        datasetfile, recognizeddata)
        trainer.train('thanks', 'evaluate')

    def commandevaluate(self):
        filemodel = './models/binary/commandmodel.h5'
        filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
        datasetfile = 'SELECT * FROM commandset'
        recognizeddata = 'SELECT * FROM recognized_commandset'
        trainer = Bot_package.Models.BinaryLSTM(filemodel, filetokenizer,
                                        datasetfile, recognizeddata)
        trainer.train('command', 'evaluate')

class Multyevaluate(Evaluate):
    def __init__(self):
        pass
    def hi_th_commandevaluate(self):
        pass
    def multyclassevaluate(self):

        trainer = Bot_package.Models.Multy('./models/multy/multyclassmodel.h5',
                                './tokenizers/multy/multyclasstokenizer.pickle',
                                'SELECT * FROM multyclasesset',
                                'SELECT * FROM recognized_multyclasesset')
        trainer.train('questionclass', 3, 'evaluate')

    def emotionsevaluate(self):
        trainer = Bot_package.Models.MultyLSTM('./models/multy/emotionsmodel.h5',
                                   './tokenizers/multy/emotionstokenizer.pickle',
                                   'SELECT * FROM emotionstrain',
                                   'SELECT * FROM recognized_emotionstrain')
        trainer.train('emotionid', 7, 'evaluate')