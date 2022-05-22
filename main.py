import telebot
import pandas as pd
import NLP
import prediction
import mapa
import subfunctions
from telebot import types
import config
import commands

#______________________________________________________________________________
hi_flag = 0
qu_flag = 0
command_flag = 0
non_flag = 0
th_flag = 0
weater_flag = 0
b_flag = 0
qnon_flag = 0
mtext = ""

#______________________________________________________________________________
API_TOKEN = '5301739662:AAEY-HVegTEbvraB_6tLN_w-Lii2aiHYylU'
boto = telebot.TeleBot(API_TOKEN)


#______________________________________________________________________________
@boto.message_handler(commands=['trainadd'])
def get_user_text(message):
    read = pd.read_excel('./datasets/dataset.xlsx')
    tstr = message.text.replace('/trainadd ', '')
    out = tstr.split('|')
    idx = 0
    for i in range(0, len(mapa.himapa)):
        if(out[1] == mapa.himapa[i]):
            idx = i
    data = {'text': NLP.libraries.preprocess_text(
        out[0]), 'agenda': out[1], 'hi': idx}
    df = pd.DataFrame(read)
    new_row = pd.Series(data)
    df = df.append(new_row, ignore_index=True)
    df.to_excel('./datasets/dataset.xlsx', index=False)

    boto.send_message(message.chat.id, 'text: ' +
                      out[0] + ' agenda: ' + out[1], parse_mode='html')

@boto.message_handler(commands=['dataset'])
def get_user_text(message):
    
    read = pd.read_excel('./datasets/dataset.xlsx')
    df = pd.DataFrame(read)
    for fram in df:
        boto.send_message(message.chat.id, fram, parse_mode='html')
#______________________________________________________________________________
def hitrain():
    filemodel = './models/binary/himodel.h5'
    filetokenizer = './tokenizers/binary/hitokenizer.pickle'
    datasetfile = './datasets/dataset.xlsx'
    NLP.binarytrain(filemodel, filetokenizer,
                    datasetfile, 'hi')
def hievaluate():
    filemodel = './models/binary/himodel.h5'
    filetokenizer = './tokenizers/binary/hitokenizer.pickle'
    datasetfile = './datasets/dataset.xlsx'
    recognizeddata = './recognized_sets/recognized_hi.xlsx'
    NLP.binaryevaluate(filemodel, filetokenizer, datasetfile, recognizeddata, 'hi')

def qutrain():
    filemodel = './models/binary/qumodel.h5'
    filetokenizer = './tokenizers/binary/qutokenizer.pickle'
    datasetfile = './datasets/questionset.xlsx'
    NLP.binarytrain(filemodel, filetokenizer, datasetfile,'question')
def quevaluate():
    filemodel = './models/binary/qumodel.h5'
    filetokenizer = './tokenizers/binary/qutokenizer.pickle'
    datasetfile = './datasets/questionset.xlsx'
    recognizeddata = './recognized_sets/recognized_qu.xlsx'
    NLP.binaryevaluate(filemodel, filetokenizer, datasetfile, recognizeddata, 'question')

def thtrain():
    filemodel = './models/binary/thmodel.h5'
    filetokenizer = './tokenizers/binary/thtokenizer.pickle'
    datasetfile = './datasets/thanksset.xlsx'
    NLP.binaryevaluate(filemodel, filetokenizer, datasetfile, 'thanks')

def thevaluate():
    filemodel = './models/binary/qumodel.h5'
    filetokenizer = './tokenizers/binary/thtokenizer.pickle'
    datasetfile = './datasets/thanksset.xlsx'
    recognizeddata = './recognized_sets/recognized_th.xlsx'
    NLP.binaryevaluate(filemodel, filetokenizer, datasetfile, recognizeddata, 'thanks')

def commandtrain():
    filemodel = './models/binary/commandmodel.h5'
    filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
    datasetfile = './datasets/commandset.xlsx'
    NLP.binarytrain(filemodel, filetokenizer, datasetfile, 'command')
def commandevaluate():
    
    filemodel = './models/binary/commandmodel.h5'
    filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
    datasetfile = './datasets/commandset.xlsx'
    recognizeddata = './recognized_sets/recognized_command.xlsx'
    NLP.binaryevaluate(filemodel, filetokenizer, datasetfile, recognizeddata, 'command')
#______________________________________________________________________________
@boto.message_handler(commands=['hitrain'])
def get_user_text(message):

    hitrain()
    boto.send_message(message.chat.id, "trained", parse_mode='html')


@boto.message_handler(commands=['qutrain'])
def get_user_text(message):
    

    qutrain()
    boto.send_message(message.chat.id, "trained", parse_mode='html')
@boto.message_handler(commands=['thtrain'])
def get_user_text(message):

    thtrain()
    boto.send_message(message.chat.id, "trained", parse_mode='html')

@boto.message_handler(commands=['commandtrain'])
def get_user_text(message):
    
    commandtrain()
    boto.send_message(message.chat.id, "trained", parse_mode='html')
#______________________________________________________________________________
@boto.message_handler(commands=['hievaluate'])
def get_user_text(message):

    hievaluate()

@boto.message_handler(commands=['quevaluate'])
def get_user_text(message):

    quevaluate()
    boto.send_message(message.chat.id, "trained", parse_mode='html')

@boto.message_handler(commands=['thevaluate'])
def get_user_text(message):

    thevaluate()
 
@boto.message_handler(commands=['commandevaluate'])
def get_user_text(message):

    commandevaluate()

#______________________________________________________________________________
@boto.message_handler(commands=['multyclasstrain'])
def get_user_text(message):
    
    NLP.multyclasstrain()
    boto.send_message(message.chat.id, "trained", parse_mode='html')
#______________________________________________________________________________
@boto.message_handler(commands=['multyclean'])
def get_user_text(message):
    NLP.DataCleaner('./datasets/multyclasesset.xlsx', 'questionclass')
    boto.send_message(message.chat.id, "cleaned", parse_mode='html')

@boto.message_handler(commands=['hiclean'])
def get_user_text(message):
    NLP.DataCleaner('./datasets/dataset.xlsx', 'hi')
    boto.send_message(message.chat.id, "cleaned", parse_mode='html')

@boto.message_handler(commands=['quclean'])
def get_user_text(message):
    NLP.QuestionsetCleaner('./datasets/questionset.xlsx')
    boto.send_message(message.chat.id, "cleaned", parse_mode='html')

@boto.message_handler(commands=['thclean'])
def get_user_text(message):
    NLP.DataCleaner('./datasets/thanksset.xlsx', 'thanks')
    boto.send_message(message.chat.id, "cleaned", parse_mode='html')

@boto.message_handler(commands=['commandclean'])
def get_user_text(message):
    
    NLP.CommandsetCleaner('./datasets/commandset.xlsx')
    boto.send_message(message.chat.id, "cleaned", parse_mode='html')
#______________________________________________________________________________
@boto.message_handler()
def get_user_text(message):
    #boto.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    global hi_flag
    global qu_flag
    global command_flag
    global non_flag
    global th_flag
    global mtext
    global weater_flag
    global b_flag
    global qnon_flag

    def set_null():
        hi_flag = 0
        qu_flag = 0
        command_flag = 0
        non_flag = 0
        th_flag = 0
        weater_flag = 0
        b_flag = 0
        qnon_flag = 0
        mtext = ""

    def button():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("👍")
        btn2 = types.KeyboardButton("👎")
        markup.add(btn1, btn2)
        return markup

    def button2():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Вопрос без класса")
        btn2 = types.KeyboardButton("Погода")
        btn3 = types.KeyboardButton("Дело")
        btn4 = types.KeyboardButton("Не вопрос")
        markup.add(btn1, btn2, btn3, btn4)
        return markup
    
    def button3():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Приветствие")
        btn2 = types.KeyboardButton("Вопрос без класса")
        btn3 = types.KeyboardButton("Погода")
        btn4 = types.KeyboardButton("Дело")
        btn5 = types.KeyboardButton("Не вопрос")
        btn6 = types.KeyboardButton("Команда")
        btn7 = types.KeyboardButton("Благодарность")
        markup.add(btn1, btn2, btn3, btn4)
        return markup
    
    def neurodesc():
        global hi_flag
        global qu_flag
        global command_flag
        global non_flag
        global th_flag
        global mtext
        global weater_flag
        global b_flag
        global qnon_flag
        if prediction.Predict(text, mapa.himapa,
                              './models/binary/himodel.h5',
                              './tokenizers/binary/hitokenizer.pickle',
                              '') == "Приветствие":

            boto.send_message(
                message.chat.id, mapa.randanswhi(), parse_mode='html', reply_markup=button())

            set_null()
            hi_flag = 1
            mtext = tstr
        elif(prediction.Predict(text, mapa.qumapa,
                                './models/binary/qumodel.h5',
                                './tokenizers/binary/qutokenizer.pickle',
                                'qu') == "Вопрос"):

            if(prediction.MultyPpredict(text) == "Дело"):
                boto.send_message(
                    message.chat.id, "Я в порядке", parse_mode='html',
                    reply_markup=button2())

                set_null()
                b_flag = 1
                qu_flag = 1
                mtext = tstr

            elif(prediction.MultyPpredict(text) == "Погода"):
                boto.send_message(
                    message.chat.id, "Погода норм", parse_mode='html',
                    reply_markup=button2())

                set_null()
                weater_flag = 1
                qu_flag = 1
                mtext = tstr

            else:
                boto.send_message(
                    message.chat.id, "Вопрос без классификации",
                    parse_mode='html', reply_markup=button2())

                set_null()
                qnon_flag = 1
                qu_flag = 1
                mtext = tstr

        elif(prediction.Predict(text, mapa.commandmapa,
                                './models/binary/commandmodel.h5',
                                './tokenizers/binary/thtokenizer.pickle',
                                'command') == "Команда"):

            reply_markup = button()

            commands.commandsdesition(boto, message, reply_markup, tstr)

            set_null()
            command_flag = 1
            mtext = tstr

        elif(prediction.Predict(text, mapa.thmapa,
                                './models/binary/thmodel.h5',
                                './tokenizers/binary/thtokenizer.pickle',
                                '') == "Благодарность"):

            boto.send_message(message.chat.id, "Не за что",
                              parse_mode='html', reply_markup=button())

            set_null()
            th_flag = 1
            mtext = tstr

        else:
            boto.send_message(
                message.chat.id, "Нет классификации", parse_mode='html',
                reply_markup=button())

            set_null()
            non_flag = 1
            mtext = tstr
            
#______________________________________________________________________________
    inpt = message.text.split(' ')

    text = []
    print(message.text)
    read = pd.read_excel('./validset/validset.xlsx')
    for txt in text:
        data = {'text': NLP.libraries.preprocess_text(txt), 'agenda': ''}
        df = pd.DataFrame(read)
        new_row = pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_excel('./validset/validset.xlsx', index=False)

    if(NLP.libraries.preprocess_text(inpt[0]) == "мис" or inpt[0].lower() == "misa"):
        tstr = message.text.replace(inpt[0], '')
        text.append(tstr)
  #      try:
            
   #     except:
    #        boto.send_message(message.chat.id, 'А?', parse_mode='html')
        neurodesc()
    elif(message.text == "👍" and hi_flag == 1):
        subfunctions.add(mtext, './recognized_sets/recognized_hi.xlsx',
                         "Приветствие", 'agenda', 'hi', 1)
        #hitrain()
        hievaluate()
        set_null()
    elif(message.text == "👎" and hi_flag == 1):
        subfunctions.add(mtext, './recognized_sets/recognized_hi.xlsx',
                         "Не приветствие", 'agenda', 'hi', 0)
        #hitrain()
        hievaluate()
        set_null()

    elif(message.text == "Вопрос без класса" and qu_flag == 1):

        subfunctions.add(mtext, './recognized_sets/recognized_multyclass.xlsx',
                         "Нет классификации", 'agenda', 'questionclass', 0)
        subfunctions.quadd(mtext, './recognized_sets/recognized_qu.xlsx',
                           "Вопрос", 1)
        #NLP.multyclasstrain()
        #qutrain()
        quevaluate()
        set_null()
    elif(message.text == "Не вопрос" and qu_flag == 1):
        subfunctions.add(mtext, './recognized_sets/recognized_multyclass.xlsx',
                         "Нет классификации", 'agenda', 'questionclass', 0)
        subfunctions.quadd(mtext, './recognized_sets/recognized_qu.xlsx',
                           "Не вопрос", 0)
        #qutrain()
        quevaluate()

        boto.send_message(message.chat.id, "Запомнила", parse_mode='html')

        set_null()
    elif(message.text == "Погода" and qu_flag == 1):
        subfunctions.add(mtext, './recognized_sets/recognized_multyclass.xlsx',
                         "Погода", 'agenda', 'questionclass', 1)
        subfunctions.quadd(mtext, './recognized_sets/recognized_qu.xlsx',
                           "Вопрос", 1)
        #NLP.multyclasstrain()
        #qutrain()
        quevaluate()

        set_null()
    elif(message.text == "Дело" and qu_flag == 1):
        subfunctions.add(mtext, './recognized_sets/recognized_multyclass.xlsx',
                         "Дело", 'agenda', 'questionclass', 1)
        subfunctions.quadd(mtext, './recognized_sets/recognized_qu.xlsx',
                           "Вопрос", 1)
        #NLP.multyclasstrain()
        qutrain()
        set_null()

    elif(message.text == "👍" and command_flag == 1):
        subfunctions.commandadd(mtext, 
                                './recognized_sets/recognized_command.xlsx',
                                "Команда", 1)

        #commandtrain()
        commandevaluate()
        set_null()

    elif(message.text == "👎" and command_flag == 1):
        subfunctions.commandadd(mtext, './recognized_sets/recognized_command.xlsx',
                                "Не команда", 0)
        #commandtrain()
        commandevaluate()
        set_null()
    elif(message.text == "👍" and th_flag == 1):
        subfunctions.add(
            mtext, './recognized_sets/recognized_th.xlsx',
            "Благодарность", 'agenda', 'thanks', 1)
        set_null()

    elif(message.text == "👎" and th_flag == 1):
        subfunctions.add(mtext, './recognized_sets/r  ecognized_th.xlsx',
                         "Не благодарность", 'agenda', 'thanks', 0)
        #thtrain()
        thevaluate()
        set_null()
    elif(message.text == "👍" and non_flag == 1):
        subfunctions.add(
            mtext, './recognized_sets/non_recognized.xlsx',
            "Нет классификации", 'agenda', 'nonclass', 1)
        #thtrain()
        #thevaluate()
        set_null()
    elif(message.text == "👎" and non_flag == 1):
        set_null()
    elif(message.text == "👎"):
        boto.send_message(message.chat.id, "😒", parse_mode='html')
    elif(message.text == "👍"):
        boto.send_message(message.chat.id, "😊", parse_mode='html')


if __name__ == '__main__':
    boto.polling(none_stop=True)



