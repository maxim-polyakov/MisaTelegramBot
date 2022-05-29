import core
import bototrain

@core.boto.message_handler(content_types=['text'])
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
        markup = core.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = core.types.KeyboardButton("👍")
        btn2 = core.types.KeyboardButton("👎")
        markup.add(btn1, btn2)
        return markup

    def button2():
        markup = core.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = core.types.KeyboardButton("Вопрос без класса")
        btn2 = core.types.KeyboardButton("Погода")
        btn3 = core.types.KeyboardButton("Дело")
        btn4 = core.types.KeyboardButton("Не вопрос")
        markup.add(btn1, btn2, btn3, btn4)
        return markup

    def button3():
        markup = core.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = core.types.KeyboardButton("Приветствие")
        btn2 = core.types.KeyboardButton("Вопрос без класса")
        btn3 = core.types.KeyboardButton("Погода")
        btn4 = core.types.KeyboardButton("Дело")
        btn5 = core.types.KeyboardButton("Не вопрос")
        btn6 = core.types.KeyboardButton("Команда")
        btn7 = core.types.KeyboardButton("Благодарность")
        markup.add(btn1, btn2, btn3, btn4)
        return markup

    def neurodesc():
        global hi_flag
        global qu_flag
        global non_flag
        global th_flag
        global mtext
        global weater_flag
        global b_flag
        global qnon_flag
        if core.prediction.Predict(text, core.mapa.himapa,
                              './models/binary/himodel.h5',
                              './tokenizers/binary/hitokenizer.pickle',
                              '') == "Приветствие":

            core.boto.send_message(
                message.chat.id, core.mapa.randanswhi(), parse_mode='html', reply_markup=button())

            set_null()
            hi_flag = 1
            mtext = tstr
        elif(core.prediction.Predict(text, core.mapa.qumapa,
                                './models/binary/qumodel.h5',
                                './tokenizers/binary/qutokenizer.pickle',
                                'qu') == "Вопрос"):

            if(core.prediction.MultyPpredict(text) == "Дело"):
                core.boto.send_message(
                    message.chat.id, "Я в порядке", parse_mode='html',
                    reply_markup=button2())

                set_null()
                b_flag = 1
                qu_flag = 1
                mtext = tstr

            elif(core.prediction.MultyPpredict(text) == "Погода"):
                core.boto.send_message(
                    message.chat.id, "Погода норм", parse_mode='html',
                    reply_markup=button2())

                set_null()
                weater_flag = 1
                qu_flag = 1
                mtext = tstr

            else:
                core.boto.send_message(
                    message.chat.id, "Вопрос без классификации",
                    parse_mode='html', reply_markup=button2())

                set_null()
                qnon_flag = 1
                qu_flag = 1
                mtext = tstr

        elif(core.prediction.Predict(text, core.mapa.commandmapa,
                                './models/binary/commandmodel.h5',
                                './tokenizers/binary/thtokenizer.pickle',
                                'command') == "Команда"):

            reply_markup = button()

            core.commands.commandsdesition(core.boto, message, reply_markup, tstr)

            set_null()
            command_flag = 1
            mtext = tstr

        elif(core.prediction.Predict(text, core.mapa.thmapa,
                                './models/binary/thmodel.h5',
                                './tokenizers/binary/thtokenizer.pickle',
                                '') == "Благодарность"):

            core.boto.send_message(message.chat.id, "Не за что",
                              parse_mode='html', reply_markup=button())

            set_null()
            th_flag = 1
            mtext = tstr

        else:
            core.boto.send_message(
                message.chat.id, "Нет классификации", parse_mode='html',
                reply_markup=button())

            set_null()
            non_flag = 1
            mtext = tstr

#______________________________________________________________________________
    inpt = message.text.split(' ')

    text = []
    print(message.text)
    read = core.pd.read_excel('./validset/validset.xlsx')
    for txt in text:
        data = {'text': core.NLP.libraries.preprocess_text(txt), 'agenda': ''}
        df = core.pd.DataFrame(read)
        new_row = core.pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_excel('./validset/validset.xlsx', index=False)
    if(core.NLP.libraries.preprocess_text(inpt[0]) == "мис" or inpt[0].lower() == "misa"):
        tstr = message.text.replace(inpt[0], '')
        text.append(tstr)
        neurodesc()
      #  try:
            
      #  except:
     #       core.boto.send_message(message.chat.id, 'А?', parse_mode='html')
    elif(message.text == "👍" and hi_flag == 1):
        core.subfunctions.add(mtext, './recognized_sets/recognized_hi.xlsx',
                         "Приветствие", 'agenda', 'hi', 1)
        #hitrain()
        bototrain.hievaluate()
        set_null()
    elif(message.text == "👎" and hi_flag == 1):
        core.subfunctions.add(mtext, './recognized_sets/recognized_hi.xlsx',
                         "Не приветствие", 'agenda', 'hi', 0)
        #hitrain()
        bototrain.hievaluate()
        set_null()
    elif(message.text == "Вопрос без класса" and qu_flag == 1):

        core.subfunctions.add(mtext, './recognized_sets/recognized_multyclass.xlsx',
                         "Нет классификации", 'agenda', 'questionclass', 0)
        core.subfunctions.quadd(mtext, './recognized_sets/recognized_qu.xlsx',
                           "Вопрос", 1)
        
        trainer = core.NLP.Multy()
        trainer.multyclasstrain('evaluate')
        #quevaluate()
        set_null()
    elif(message.text == "Не вопрос" and qu_flag == 1):
        core.subfunctions.add(mtext, './recognized_sets/recognized_multyclass.xlsx',
                         "Нет классификации", 'agenda', 'questionclass', 0)
        core.subfunctions.quadd(mtext, './recognized_sets/recognized_qu.xlsx',
                           "Не вопрос", 0)
        #qutrain()
        bototrain.quevaluate()

        core.boto.send_message(message.chat.id, "Запомнила", parse_mode='html')

        set_null()
    elif(message.text == "Погода" and qu_flag == 1):
        core.subfunctions.add(mtext, './recognized_sets/recognized_multyclass.xlsx',
                         "Погода", 'agenda', 'questionclass', 1)
        core.subfunctions.quadd(mtext, './recognized_sets/recognized_qu.xlsx',
                           "Вопрос", 1)
        
        trainer = core.NLP.Multy()
        trainer.multyclasstrain('evaluate')
        set_null()
    elif(message.text == "Дело" and qu_flag == 1):
        core.subfunctions.add(mtext, './recognized_sets/recognized_multyclass.xlsx',
                         "Дело", 'agenda', 'questionclass', 1)
        core.subfunctions.quadd(mtext, './recognized_sets/recognized_qu.xlsx',
                           "Вопрос", 1)
        
        trainer = core.NLP.Multy()
        trainer.multyclasstrain('evaluate')
        bototrain.qutrain()
        set_null()
    elif(message.text == "👍" and command_flag == 1):
        core.subfunctions.commandadd(mtext,
                                './recognized_sets/recognized_command.xlsx',
                                "Команда", 1)
        bototrain.commandevaluate()
        set_null()
    elif(message.text == "👎" and command_flag == 1):
        core.subfunctions.commandadd(mtext, './recognized_sets/recognized_command.xlsx',
                                "Не команда", 0)
        bototrain.commandevaluate()
        set_null()
    elif(message.text == "👍" and th_flag == 1):
        core.subfunctions.add(
            mtext, './recognized_sets/recognized_th.xlsx',
            "Благодарность", 'agenda', 'thanks', 1)
        set_null()
    elif(message.text == "👎" and th_flag == 1):
        core.subfunctions.add(mtext, './recognized_sets/r  ecognized_th.xlsx',
                         "Не благодарность", 'agenda', 'thanks', 0)
        bototrain.thevaluate()
        set_null()
    elif(message.text == "👍" and non_flag == 1):
        core.subfunctions.add(
            mtext, './recognized_sets/non_recognized.xlsx',
            "Нет классификации", 'agenda', 'nonclass', 1)
        set_null()
    elif(message.text == "👎" and non_flag == 1):
        set_null()
    elif(message.text == "👎"):
        core.boto.send_message(message.chat.id, "😒", parse_mode='html')
    elif(message.text == "👍"):
        core.boto.send_message(message.chat.id, "😊", parse_mode='html')