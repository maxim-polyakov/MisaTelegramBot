import core
import messagemonitor
#import pyTelegramBotAPI
#______________________________________________________________________________


#______________________________________________________________________________
@core.boto.message_handler(commands=['trainadd'])
def get_user_text(message):
    read = core.pd.read_excel('./datasets/dataset.xlsx')
    tstr = message.text.replace('/trainadd ', '')
    out = tstr.split('|')
    idx = 0
    for i in range(0, len(core.mapa.himapa)):
        if(out[1] == core.mapa.himapa[i]):
            idx = i
    data = {'text': core.NLP.libraries.preprocess_text(
        out[0]), 'agenda': out[1], 'hi': idx}
    df = core.pd.DataFrame(read)
    new_row = core.pd.Series(data)
    df = df.append(new_row, ignore_index=True)
    df.to_excel('./datasets/dataset.xlsx', index=False)

    core.boto.send_message(message.chat.id, 'text: ' +
                      out[0] + ' agenda: ' + out[1], parse_mode='html')




@core.boto.message_handler(commands=['dataset'])
def get_user_text(message):

    read = core.pd.read_excel('./datasets/dataset.xlsx')
    df = core.pd.DataFrame(read)
    for fram in df:
        core.boto.send_message(message.chat.id, fram, parse_mode='html')
#______________________________________________________________________________


def hitrain():
    filemodel = './models/binary/himodel.h5'
    filetokenizer = './tokenizers/binary/hitokenizer.pickle'
    datasetfile = './datasets/dataset.xlsx'
    recognizeddata = './recognized_sets/recognized_hi.xlsx'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('hi','train')


def hievaluate():
    filemodel = './models/binary/himodel.h5'
    filetokenizer = './tokenizers/binary/hitokenizer.pickle'
    datasetfile = './datasets/dataset.xlsx'
    recognizeddata = './recognized_sets/recognized_hi.xlsx'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('hi','evaluate')


def qutrain():
    filemodel = './models/binary/qumodel.h5'
    filetokenizer = './tokenizers/binary/qutokenizer.pickle'
    datasetfile = './datasets/questionset.xlsx'
    recognizeddata = './recognized_sets/recognized_qu.xlsx'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('question','train')


def quevaluate():
    filemodel = './models/binary/qumodel.h5'
    filetokenizer = './tokenizers/binary/qutokenizer.pickle'
    datasetfile = './datasets/questionset.xlsx'
    recognizeddata = './recognized_sets/recognized_qu.xlsx'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('question','evaluate')


def thtrain():
    filemodel = './models/binary/thmodel.h5'
    filetokenizer = './tokenizers/binary/thtokenizer.pickle'
    datasetfile = './datasets/thanksset.xlsx'
    recognizeddata = './recognized_sets/recognized_th.xlsx'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('thanks','train')


def thevaluate():
    filemodel = './models/binary/qumodel.h5'
    filetokenizer = './tokenizers/binary/thtokenizer.pickle'
    datasetfile = './datasets/thanksset.xlsx'
    recognizeddata = './recognized_sets/recognized_th.xlsx'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('thanks','evaluate')


def commandtrain():
    filemodel = './models/binary/commandmodel.h5'
    filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
    datasetfile = './datasets/commandset.xlsx'
    recognizeddata = './recognized_sets/recognized_command.xlsx'
    trainer = core.NLP.Binary(filemodel, filetokenizer, datasetfile, recognizeddata)
    trainer.binary('command','train')


def commandevaluate():
    filemodel = './models/binary/commandmodel.h5'
    filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
    datasetfile = './datasets/commandset.xlsx'
    recognizeddata = './recognized_sets/recognized_command.xlsx'
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
#______________________________________________________________________________


@core.boto.message_handler(commands=['multyclasstrain'])
def get_user_text(message):

    trainer = core.NLP.Multy()
    trainer.multyclasstrain('train')
    core.boto.send_message(message.chat.id, "trained", parse_mode='html')
#______________________________________________________________________________


@core.boto.message_handler(commands=['multyclean'])
def get_user_text(message):
    core.NLP.DataCleaner('./datasets/multyclasesset.xlsx', 'questionclass')
    core.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@core.boto.message_handler(commands=['hiclean'])
def get_user_text(message):
    core.NLP.DataCleaner('./datasets/dataset.xlsx', 'hi')
    core.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@core.boto.message_handler(commands=['quclean'])
def get_user_text(message):
    core.NLP.QuestionsetCleaner('./datasets/questionset.xlsx')
    core.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@core.boto.message_handler(commands=['thclean'])
def get_user_text(message):
    core.NLP.DataCleaner('./datasets/thanksset.xlsx', 'thanks')
    core.boto.send_message(message.chat.id, "cleaned", parse_mode='html')


@core.boto.message_handler(commands=['commandclean'])
def get_user_text(message):

    core.NLP.CommandsetCleaner('./datasets/commandset.xlsx')
    core.boto.send_message(message.chat.id, "cleaned", parse_mode='html')
#______________________________________________________________________________





if __name__ == "__main__":
    #boto.polling(none_stop=True)
    core.boto.remove_webhook()
    core.time.sleep(1)
    core.boto.set_webhook(url = core.WEB_HOOK_URL)
    core.app.run(host = core.APP_HOST, port = core.APP_PORT, debug = False)



