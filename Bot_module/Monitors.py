import bot
from bot import subfunctions
from bot import bototrain
import psycopg2
from sqlalchemy import create_engine
import Bot_module


class Monitor:
    def __init__(self):
        pass

    def monitor(self):
        pass


class MessageMonitor(Monitor):

    __hi_flag = 0
    __qu_flag = 0
    __command_flag = 0
    __non_flag = 0
    __th_flag = 0
    __weater_flag = 0
    __b_flag = 0
    __q__non_flag = 0
    __mtext = ""

    def __init__(self, message):
        self.__message = message

    def __set_null(self, ):
        self.__hi_flag = 0
        self.__qu_flag = 0
        self.__command_flag = 0
        self.__non_flag = 0
        self.__th_flag = 0
        self.__weater_flag = 0
        self.__b_flag = 0
        self.__q__non_flag = 0
        self.__mtext = ""

    def __neurodesc(self, text, tstr):

        conn = psycopg2.connect(
            "dbname=postgres user=postgres password=postgres")
        df = bot.pd.read_sql('SELECT text FROM commands', conn)
        Cdict = df['text'].to_dict()

        bpred = bot.Predictors.Binary()
        mpred = bot.Predictors.Multy()
        qpr = bot.Models.TextPreprocessers.QuestionPreprocessing()
        cpr = bot.Models.TextPreprocessers.CommandPreprocessing()
        ststr = qpr.reversepreprocess_text(self.__message.text)
        a = cpr.preprocess_text(text[0])
        splta = a.split()
        print("splta = ", splta[0])
        if (len(ststr) > 0 and self.__message.text.count('?') > 0):
            if(mpred.predict(text, bot.mapa.multymapa,
                             './models/multy/multyclassmodel.h5',
                             './tokenizers/multy/multyclasstokenizer.pickle') == "Дело"):
                bot.boto.send_message(
                    self.__message.chat.id, "Я в порядке", parse_mode='html')

                self.__set_null()
                self.__b_flag = 1
                self.__qu_flag = 1
                self.__mtext = tstr

            elif(mpred.predict(text, bot.mapa.multymapa,
                               './models/multy/multyclassmodel.h5',
                               './tokenizers/multy/multyclasstokenizer.pickle') == "Погода"):
                bot.boto.send_message(
                    self.__message.chat.id, "Погода норм", parse_mode='html')

                self.__set_null()
                self.__weater_flag = 1
                self.__qu_flag = 1
                self.__mtext = tstr

            else:
                bot.boto.send_message(
                    self.__message.chat.id, "Вопрос без классификации",
                    parse_mode='html')

                bot.commands.commandsdesition(
                    bot.boto, text, tstr)
                self.__set_null()
                self.__q__non_flag = 1
                self.__qu_flag = 1
                self.__mtext = tstr
        elif(splta[0] in Cdict.values()):

            if(bpred.predict(text, bot.mapa.commandmapa,
                             './models/binary/commandmodel.h5',
                             './tokenizers/binary/thtokenizer.pickle',
                             'command') == "Команда"):
                self.__set_null()
                self.__command_flag = 1
                print(self.__command_flag)
                bot.commands.commandsdesition(
                    bot.boto, self.__message, tstr)
            else:
                bot.boto.send_message(
                    self.__message.chat.id, "Похоже на команду но я не уверена.",
                    parse_mode='html')

            self.__mtext = tstr
        elif(bpred.predict(text, bot.mapa.himapa,
                           './models/binary/himodel.h5',
                           './tokenizers/binary/hitokenizer.pickle',
                           '') == "Приветствие"):

            ra = bot.Answers.RandomAnswer()
            bot.boto.send_message(
                self.__message.chat.id, ra.answer(), parse_mode='html')

            self.__set_null()
            self.__hi_flag = 1
            self.__mtext = tstr

        elif(bpred.predict(text, bot.mapa.thmapa,
                           './models/binary/thmodel.h5',
                           './tokenizers/binary/thtokenizer.pickle',
                           '') == "Благодарность"):

            bot.boto.send_message(self.__message.chat.id, "Не за что",
                                  parse_mode='html')

            self.__set_null()
            self.__th_flag = 1
            self.__mtext = tstr
        else:

            if(mpred.predict(text, bot.mapa.multymapa, './models/multy/multyclassmodel.h5',
                             './tokenizers/multy/multyclasstokenizer.pickle') == "Дело"):
                bot.boto.send_message(
                    self.__message.chat.id, "Утверждение про дела", parse_mode='html')

            elif(mpred.predict(text, bot.mapa.multymapa, './models/multy/multyclassmodel.h5',
                               './tokenizers/multy/multyclasstokenizer.pickle') == "Погода"):
                bot.boto.send_message(
                    self.__message.chat.id, "Утверждение про погоду", parse_mode='html')
            else:
                bot.boto.send_message(
                    self.__message.chat.id, "Нет классификации",
                    parse_mode='html')

            self.__set_null()
            self.__non_flag = 1
            self.__mtext = tstr

    def monitor(self):

        inpt = self.__message.text.split(' ')

        text = []
        print(self.__message.text)
        pr = bot.Models.TextPreprocessers.CommonPreprocessing()

        if(self.__message.text.lower().count('миса') > 0 or self.__message.text.lower().count('misa') > 0):
            tstr = self.__message.text.replace("миса", '')
            ststr = tstr.replace("misa", '')
            text.append(ststr)

            for txt in text:
                conn = psycopg2.connect(
                    "dbname=postgres user=postgres password=postgres")
                engine = create_engine(
                    'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')

                data = {'text': pr.preprocess_text(txt), 'agenda': ''}
                df = bot.pd.DataFrame()
                new_row = bot.pd.Series(data)
                df = df.append(new_row, ignore_index=True)
                print(df)
                df.to_sql('validset', con=engine, schema='public',
                          index=False, if_exists='append')
            try:
                self.__neurodesc(text, tstr)
            except:
                bot.boto.send_message(
                    self.__message.chat.id, 'А?', parse_mode='html')
        elif(self.__message.text == "👍" and self.__hi_flag == 1):
            subfunctions.add(self.__mtext, 'recognized_hi',
                             "Приветствие", 'agenda', 'hi', 1)
            # hitrain()
            bototrain.hievaluate()
            self.__set_null()
        elif(self.__message.text == "👎" and self.__hi_flag == 1):
            subfunctions.add(self.__mtext, 'recognized_hi',
                             "Не приветствие", 'agenda', 'hi', 0)
            # hitrain()
            bototrain.hievaluate()
            self.__set_null()
        elif(self.__message.text == "Вопрос без класса" and self.__qu_flag == 1):

            subfunctions.add(self.__mtext, 'recognized_multyclass',
                             "Нет классификации", 'agenda', 'questionclass', 0)
            subfunctions.quadd(self.__mtext, 'recognized_qu',
                               "Вопрос", 1)

            trainer = bot.Models.Multy()
            trainer.multyclasstrain('evaluate')
            # quevaluate()
            self.__set_null()
        elif(self.__message.text == "Не вопрос" and self.__qu_flag == 1):
            subfunctions.add(self.__mtext, 'recognized_multyclass',
                             "Нет классификации", 'agenda', 'questionclass', 0)
            subfunctions.quadd(self.__mtext, 'recognized_qu',
                               "Не вопрос", 0)
            # qutrain()
            bototrain.quevaluate()

            bot.boto.send_message(
                self.__message.chat.id, "Запомнила", parse_mode='html')

            self.__set_null()
        elif(self.__message.text == "Погода" and self.__qu_flag == 1):
            subfunctions.add(self.__mtext, 'recognized_multyclass',
                             "Погода", 'agenda', 'questionclass', 1)
            subfunctions.quadd(self.__mtext, 'recognized_qu',
                               "Вопрос", 1)

            trainer = bot.NLP.Multy('./models/multy/multyclassmodel.h5',
                                    './tokenizers/multy/multyclasstokenizer.pickle',
                                    'SELECT * FROM multyclasesset',
                                    'SELECT * FROM recognized_multyclass')
            trainer.train('questionclass', 3, 'evaluate')
            self.__set_null()
        elif(self.__message.text == "Дело" and self.__qu_flag == 1):
            subfunctions.add(self.__mtext, 'recognized_multyclass',
                             "Дело", 'agenda', 'questionclass', 1)
            subfunctions.quadd(self.__mtext, 'recognized_qu',
                               "Вопрос", 1)

            trainer = bot.NLP.Multy('./models/multy/multyclassmodel.h5',
                                    './tokenizers/multy/multyclasstokenizer.pickle',
                                    'SELECT * FROM multyclasesset',
                                    'SELECT * FROM recognized_multyclass')
            trainer.train('questionclass', 3, 'evaluate')

          #  bototrain.quevaluate()
            self.__set_null()
        elif(self.__message.text == "👍" and self.__command_flag == 1):
            subfunctions.commandadd(self.__mtext,
                                    'recognized_command',
                                    "Команда", 1)
            bototrain.commandevaluate()
            self.__set_null()
        elif(self.__message.text == "👎" and self.__command_flag == 1):
            subfunctions.commandadd(self.__mtext, 'recognized_command',
                                    "Не команда", 0)
            bototrain.commandevaluate()
            self.__set_null()
        elif(self.__message.text == "👍" and self.__th_flag == 1):
            subfunctions.add(
                self.__mtext, 'recognized_th',
                "Благодарность", 'agenda', 'thanks', 1)
            self.__set_null()
        elif(self.__message.text == "👎" and self.__th_flag == 1):
            subfunctions.add(self.__mtext, 'recognized_th',
                             "Не благодарность", 'agenda', 'thanks', 0)
            bototrain.thevaluate()
            self.__set_null()
        elif(self.__message.text == "👍" and self.__non_flag == 1):
            subfunctions.add(
                self.__mtext, 'non_recognized',
                "Нет классификации", 'agenda', 'nonclass', 1)
            self.__set_null()
        elif(self.__message.text == "👎" and self.__non_flag == 1):
            self.__set_null()
        elif(self.__message.text == "👎"):
            bot.boto.send_message(self.__message.chat.id,
                                  "😒", parse_mode='html')
        elif(self.__message.text == "👍"):
            bot.boto.send_message(self.__message.chat.id,
                                  "😊", parse_mode='html')
