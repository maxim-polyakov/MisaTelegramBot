import bot
from bot import subfunctions
from bot import bototrain
from sqlalchemy import create_engine


hi_flag = 0
qu_flag = 0
command_flag = 0
non_flag = 0
th_flag = 0
weater_flag = 0
b_flag = 0
qnon_flag = 0
mtext = ""


@bot.boto.message_handler(content_types=['text'])
def get_user_text(message):
    # boto.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
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



    def neurodesc():
        global hi_flag
        global qu_flag
        global non_flag
        global th_flag
        global mtext
        global weater_flag
        global b_flag
        global qnon_flag

        bpred = bot.Predictors.Binary()
        mpred = bot.Predictors.Multy()
        qpr = bot.Models.TextPreprocessers.QuestionPreprocessing()
        #bpred.predict(text, bot.mapa.qumapa,'./models/binary/qumodel.h5', './tokenizers/binary/qutokenizer.pickle','qu') == "Вопрос" or 
        ststr = qpr.reversepreprocess_text(message.text)

        if bpred.predict(text, bot.mapa.himapa,
                         './models/binary/himodel.h5',
                         './tokenizers/binary/hitokenizer.pickle',
                         '') == "Приветствие":

            ra = bot.Answers.RandomAnswer()
            bot.boto.send_message(
                message.chat.id, ra.answer(), parse_mode='html')

            set_null()
            hi_flag = 1
            mtext = tstr
        elif(len(ststr) > 0 and message.text.count('?') > 0):
            if(mpred.predict(text) == "Дело"):
                bot.boto.send_message(
                    message.chat.id, "Я в порядке", parse_mode='html')

                set_null()
                b_flag = 1
                qu_flag = 1
                mtext = tstr

            elif(mpred.predict(text) == "Погода"):
                bot.boto.send_message(
                    message.chat.id, "Погода норм", parse_mode='html')

                set_null()
                weater_flag = 1
                qu_flag = 1
                mtext = tstr

            else:
                bot.boto.send_message(
                    message.chat.id, "Вопрос без классификации",
                    parse_mode='html')

                set_null()
                qnon_flag = 1
                qu_flag = 1
                mtext = tstr

        elif(bpred.predict(text, bot.mapa.commandmapa,
                           './models/binary/commandmodel.h5',
                           './tokenizers/binary/thtokenizer.pickle',
                           'command') == "Команда"):

            set_null()
            command_flag = 1
            print(command_flag)
            bot.commands.commandsdesition(
                bot.boto, message, tstr)

            mtext = tstr

        elif(bpred.predict(text, bot.mapa.thmapa,
                           './models/binary/thmodel.h5',
                           './tokenizers/binary/thtokenizer.pickle',
                           '') == "Благодарность"):

            bot.boto.send_message(message.chat.id, "Не за что",
                                  parse_mode='html')

            set_null()
            th_flag = 1
            mtext = tstr

        else:
            if(mpred.predict(text) == "Дело"):
                bot.boto.send_message(
                    message.chat.id, "Утверждение про дела", parse_mode='html')

            elif(mpred.predict(text) == "Погода"):
                bot.boto.send_message(
                    message.chat.id, "Утверждение про погоду", parse_mode='html')
            else:
                bot.boto.send_message(
                    message.chat.id, "Нет классификации",
                    parse_mode='html')

            set_null()
            non_flag = 1
            mtext = tstr

# ______________________________________________________________________________
    inpt = message.text.split(' ')

    text = []
    print(message.text)
    pr = bot.Models.TextPreprocessers.CommonPreprocessing()
    for txt in text:
        conn = bot.NLP.psycopg2.connect("dbname=postgres user=postgres password=postgres")
        engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
        
        data = {'text': pr.preprocess_text(txt), 'agenda': ''}
        df = bot.pd.DataFrame()
        new_row = bot.pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql('validset', con = engine, schema = 'public', index=False, if_exists='append')

    if(pr.preprocess_text(inpt[0]) == "мис" or inpt[0].lower() == "misa"):
        tstr = message.text.replace(inpt[0], '')
        text.append(tstr)
        neurodesc()
      #  try:

     #   except:
     #       bot.boto.send_message(message.chat.id, 'А?', parse_mode='html')
    elif(message.text == "👍" and hi_flag == 1):
        subfunctions.add(mtext, 'recognized_hi',
                         "Приветствие", 'agenda', 'hi', 1)
        # hitrain()
        bototrain.hievaluate()
        set_null()
    elif(message.text == "👎" and hi_flag == 1):
        subfunctions.add(mtext, 'recognized_hi',
                         "Не приветствие", 'agenda', 'hi', 0)
        # hitrain()
        bototrain.hievaluate()
        set_null()
    elif(message.text == "Вопрос без класса" and qu_flag == 1):

        subfunctions.add(mtext, 'recognized_multyclass',
                         "Нет классификации", 'agenda', 'questionclass', 0)
        subfunctions.quadd(mtext, 'recognized_qu',
                           "Вопрос", 1)

        trainer = bot.Models.Multy()
        trainer.multyclasstrain('evaluate')
        # quevaluate()
        set_null()
    elif(message.text == "Не вопрос" and qu_flag == 1):
        subfunctions.add(mtext, 'recognized_multyclass',
                         "Нет классификации", 'agenda', 'questionclass', 0)
        subfunctions.quadd(mtext, 'recognized_qu',
                           "Не вопрос", 0)
        # qutrain()
        bototrain.quevaluate()

        bot.boto.send_message(message.chat.id, "Запомнила", parse_mode='html')

        set_null()
    elif(message.text == "Погода" and qu_flag == 1):
        subfunctions.add(mtext, 'recognized_multyclass',
                         "Погода", 'agenda', 'questionclass', 1)
        subfunctions.quadd(mtext, 'recognized_qu',
                           "Вопрос", 1)

        trainer = bot.NLP.Multy()
        trainer.train('evaluate')
        set_null()
    elif(message.text == "Дело" and qu_flag == 1):
        subfunctions.add(mtext, 'recognized_multyclass',
                         "Дело", 'agenda', 'questionclass', 1)
        subfunctions.quadd(mtext, 'recognized_qu',
                           "Вопрос", 1)

        trainer = bot.Models.Multy()
        trainer.train('evaluate')
        bototrain.qutrain()
        set_null()
    elif(message.text == "👍" and command_flag == 1):
        subfunctions.commandadd(mtext,
                                'recognized_command',
                                "Команда", 1)
        bototrain.commandevaluate()
        set_null()
    elif(message.text == "👎" and command_flag == 1):
        subfunctions.commandadd(mtext, 'recognized_command',
                                "Не команда", 0)
        bototrain.commandevaluate()
        set_null()
    elif(message.text == "👍" and th_flag == 1):
        subfunctions.add(
            mtext, 'recognized_th',
            "Благодарность", 'agenda', 'thanks', 1)
        set_null()
    elif(message.text == "👎" and th_flag == 1):
        subfunctions.add(mtext, 'recognized_th',
                         "Не благодарность", 'agenda', 'thanks', 0)
        bototrain.thevaluate()
        set_null()
    elif(message.text == "👍" and non_flag == 1):
        subfunctions.add(
            mtext, 'non_recognized',
            "Нет классификации", 'agenda', 'nonclass', 1)
        set_null()
    elif(message.text == "👎" and non_flag == 1):
        set_null()
    elif(message.text == "👎"):
        bot.boto.send_message(message.chat.id, "😒", parse_mode='html')
    elif(message.text == "👍"):
        bot.boto.send_message(message.chat.id, "😊", parse_mode='html')
