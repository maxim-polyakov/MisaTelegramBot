import telebot
import pandas as pd
import NLP
import prediction
import mapa
import subfunctions
from telebot import types
import config

# Классификация
boto = telebot.TeleBot('5301739662:AAG4EZfZtvPkku9b9eymTHZW6EITYyKuAbc')

hi_flag = 0
qu_flag = 0
command_flag = 0
non_flag = 0
th_flag = 0
weater_flag = 0
b_flag = 0
qnon_flag = 0
mtext = ""


@boto.message_handler(commands=['start'])
def start(message):
    mess = f'Hi, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
    boto.send_message(message.chat.id, mess,  parse_mode='html')


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


@boto.message_handler(commands=['hitrain'])
def get_user_text(message):

    filemodel = './models/binary/himodel.h5'
    filetokenizer = './tokenizers/binary/hitokenizer.pickle'
    datasetfile = './datasets/dataset.xlsx'
    NLP.binarytrain(filemodel, filetokenizer, datasetfile, 'hi')
    boto.send_message(message.chat.id, "trained", parse_mode='html')


@boto.message_handler(commands=['qutrain'])
def get_user_text(message):

    filemodel = './models/binary/qumodel.h5'
    filetokenizer = './tokenizers/binary/qutokenizer.pickle'
    datasetfile = './datasets/questionset.xlsx'
    NLP.binarytrain(filemodel, filetokenizer, datasetfile, 'question')
    boto.send_message(message.chat.id, "trained", parse_mode='html')


@boto.message_handler(commands=['thtrain'])
def get_user_text(message):

    filemodel = './models/binary/thmodel.h5'
    filetokenizer = './tokenizers/binary/thtokenizer.pickle'
    datasetfile = './datasets/thanksset.xlsx'
    NLP.binarytrain(filemodel, filetokenizer, datasetfile, 'thanks')
    boto.send_message(message.chat.id, "trained", parse_mode='html')


@boto.message_handler(commands=['commandtrain'])
def get_user_text(message):
    filemodel = './models/binary/commandmodel.h5'
    filetokenizer = './tokenizers/binary/commandtokenizer.pickle'
    datasetfile = './datasets/commandset.xlsx'
    NLP.binarytrain(filemodel, filetokenizer, datasetfile, 'command')
    boto.send_message(message.chat.id, "trained", parse_mode='html')


@boto.message_handler(commands=['multyclasstrain'])
def get_user_text(message):
    NLP.multyclasstrain()
    boto.send_message(message.chat.id, "trained", parse_mode='html')


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


@boto.message_handler()
def get_user_text(message):

    global hi_flag
    global qu_flag
    global command_flag
    global non_flag
    global th_flag
    global mtext
    global weater_flag
    global b_flag
    global qnon_flag

    def button():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Угадала")
        btn2 = types.KeyboardButton("Не угадала")
        markup.add(btn1, btn2)
        return markup

    inpt = message.text.split(' ')

    text = []

    read = pd.read_excel('./validset/validset.xlsx')
    for txt in text:
        data = {'text': NLP.libraries.preprocess_text(txt), 'agenda': ''}
        df = pd.DataFrame(read)
        new_row = pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_excel('./validset/validset.xlsx', index=False)

    if(inpt[0].lower() == "миса" or inpt[0].lower() == "misa"):
        tstr = message.text.replace(inpt[0], '')
        text.append(tstr)
        try:
            if prediction.Predict(text, mapa.himapa,
                                  './models/binary/himodel.h5',
                                  './tokenizers/binary/hitokenizer.pickle',
                                  '') == "Приветствие":

                boto.send_message(
                    message.chat.id, mapa.randanswhi(), parse_mode='html')
                boto.send_message(
                    message.chat.id, "Угадала что "
                    + prediction.preprocessing(text, '').pop() + " - привет?",
                    parse_mode='html', reply_markup=button())

                hi_flag = 1
                mtext = tstr
            elif(prediction.Predict(text, mapa.qumapa,
                                    './models/binary/qumodel.h5',
                                    './tokenizers/binary/qutokenizer.pickle',
                                    'qu') == "Вопрос"):

                if(prediction.MultyPpredict(text) == "Дело"):
                    boto.send_message(
                        message.chat.id, "Я в порядке", parse_mode='html')

                    boto.send_message(
                        message.chat.id, "Угадала что "
                        + prediction.preprocessing(text, 'qu').pop() +
                        " - вопрос про погоду?", parse_mode='html',
                        reply_markup=button())
                    boto.send_message(
                        message.chat.id, "Угадала что "
                        + prediction.preprocessing(text, 'qu').pop() +
                        " - вопрос про дела?", parse_mode='html',
                        reply_markup=button())
                    b_flag = 1
                    qu_flag = 1
                    mtext = tstr

                elif(prediction.MultyPpredict(text) == "Погода"):
                    boto.send_message(
                        message.chat.id, "Погода норм", parse_mode='html')

                    boto.send_message(
                        message.chat.id, "Угадала что "
                        + prediction.preprocessing(text, 'qu').pop() +
                        " - вопрос про погоду?", parse_mode='html',
                        reply_markup=button())
                    weater_flag = 1
                    qu_flag = 1
                    mtext = tstr

                else:
                    boto.send_message(
                        message.chat.id, "Вопрос без классификации",
                        parse_mode='html')

                    boto.send_message(
                        message.chat.id, "Угадала что "
                        + prediction.preprocessing(text, 'qu').pop() +
                        " - вопрос без классификации?", parse_mode='html',
                        reply_markup=button())
                    qnon_flag = 1
                    qu_flag = 1
                    mtext = tstr


            elif(prediction.Predict(text, mapa.commandmapa,
                                    './models/binary/commandmodel.h5',
                                    './tokenizers/binary/thtokenizer.pickle',
                                    'command') == "Команда"):
                boto.send_message(
                    message.chat.id, "Команда", parse_mode='html')

                boto.send_message(
                    message.chat.id, "Угадала что"
                    + prediction.preprocessing(text, 'command').pop()
                    + " - команда?", parse_mode='html',
                    reply_markup=button())
                command_flag = 1
                mtext = tstr

            elif(prediction.Predict(text, mapa.thmapa,
                                    './models/binary/thmodel.h5',
                                    './tokenizers/binary/thtokenizer.pickle',
                                    '') == "Благодарность"):

                boto.send_message(message.chat.id, "Не за что",
                                  parse_mode='html')

                boto.send_message(
                    message.chat.id, "Угадала что "
                    + prediction.preprocessing(text, '').pop()
                    + " - благодарность?", parse_mode='html',
                    reply_markup=button())
            else:
                boto.send_message(
                    message.chat.id, "Нет классификации", parse_mode='html')

                boto.send_message(
                    message.chat.id, "Угадала что у"
                    + prediction.preprocessing(text, '').pop()
                    + " нет классификации?", parse_mode='html',
                    reply_markup=button())
                non_flag = 1
                mtext = tstr
        except:
            boto.send_message(message.chat.id, 'А?', parse_mode='html')

    elif(message.text == "Угадала" and hi_flag == 1):
        subfunctions.add(mtext, './recognized_sets/recognized_hi.xlsx',
            "Приветствие", 'agenda', 'hi', 1)
        hi_flag = 0
    elif(message.text == "Не угадала" and hi_flag == 1):
        subfunctions.add(mtext, './recognized_sets/recognized_hi.xlsx',
            "Не приветствие", 'agenda', 'hi', 0)

    elif(message.text == "Угадала" and qu_flag == 1):
        subfunctions.quadd(
            mtext, './recognized_sets/recognized_qu.xlsx',
            "Вопрос", 1)
        
        if(message.text == "Угадала" and weater_flag == 1 and b_flag == 0):
            subfunctions.add(
                mtext, './recognized_sets/recognized_multyclass.xlsx',
                "Погода", 'agenda', 'questionclass', 1)
            weater_flag = 0

        elif(message.text == "Не угадала" and weater_flag == 1 and b_flag == 0):
            subfunctions.add(mtext, './recognized_sets/recognized_multyclass.xlsx',
                "Не погода", 'agenda', 'questionclass', 0)

        elif(message.text == "Угадала" and b_flag == 1 and weater_flag == 0):
            subfunctions.add(
                mtext, './recognized_sets/recognized_multyclass.xlsx',
                "Дело", 'agenda', 'questionclass', 2)
            b_flag = 0

        elif(message.text == "Не угадала" and b_flag == 1 and weater_flag == 0):
            subfunctions.add(mtext, './recognized_sets/recognized_multyclass.xlsx',
                "Не Дело", 'agenda', 'questionclass', 0)
        elif(message.text == "Угадала" and qnon_flag == 1):
            subfunctions.add(mtext, './recognized_sets/recognized_multyclass.xlsx',
                "Нет классификации", 'agenda', 'questionclass', 0)
            qnon_flag = 0

        qu_flag = 0
    elif(message.text == "Не угадала" and qu_flag == 1 and (b_flag == 0 and weater_flag == 0 and qnon_flag == 0)):
        subfunctions.quadd(
            mtext, './recognized_sets/recognized_qu.xlsx',
            "Не вопрос", 0)

    elif(message.text == "Угадала" and command_flag == 1):
        subfunctions.add(
            mtext, './recognized_sets/recognized_command.xlsx',
            "Команда", 'agenda', 'command', 1)
        command_flag = 0

    elif(message.text == "Не угадала" and command_flag == 1):
        subfunctions.add(mtext, './recognized_sets/recognized_command.xlsx',
            "Не команда", 'agenda', 'command', 0)

    elif(message.text == "Угадала" and th_flag == 1):
        subfunctions.add(
            mtext, './recognized_sets/recognized_th.xlsx',
            "Благодарность", 'agenda', 'thanks', 1)
        th_flag = 0

    elif(message.text == "Не угадала" and th_flag == 1):
        subfunctions.add(mtext, './recognized_sets/recognized_th.xlsx',
            "Не благодарность", 'agenda', 'thanks', 0)

    elif(message.text == "Угадала" and non_flag == 1):
        subfunctions.add(
            mtext, './recognized_sets/non_recognized.xlsx',
            "Нет классификации", 'agenda', 'nonclass', 1)
        non_flag = 0

    elif(message.text == "Не угадала" and non_flag == 1):
        subfunctions.add(mtext, './recognized_sets/non_recognized.xlsx',
        "Нет классификации", 'agenda', 'nonclass', 0)


boto.polling(none_stop=True)
