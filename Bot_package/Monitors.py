import bot
import psycopg2
from sqlalchemy import create_engine
from Bot_package import Subfunctions
from Bot_package import Bototrainers
from Bot_package import Botoevaluaters
from Command_package import Commands

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

    __bpred = bot.Predictors.Binary()
    __nnpred = bot.Predictors.NonNeuro()
    __mpred = bot.Predictors.Multy()
    __qpr = bot.Models.TextPreprocessers.QuestionPreprocessing()
    __cpr = bot.Models.TextPreprocessers.CommandPreprocessing()
    __pr = bot.Models.TextPreprocessers.CommonPreprocessing()
    
    _engine = create_engine(
                    'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
    _conn = psycopg2.connect(
        "dbname=postgres user=postgres password=postgres")

    __ad = Subfunctions.Adder()
    __bt = Bototrainers.Train()
    __mt = Bototrainers.Multytrain()
    __be = Botoevaluaters.Binaryevaluate()
    __me = Botoevaluaters.Multyevaluate()
    __mapa = bot.Mapas.Mapa()

    def __init__(self, message):
        self.__message = message

    def __set_null(self):
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

        df = bot.pd.read_sql('SELECT text FROM commands', self._conn)
        Cdict = df['text'].to_dict()

        ststr = self.__qpr.reversepreprocess_text(tstr)
        a = self.__cpr.preprocess_text(text[0])
        splta = a.split()

        print("splta = ", splta[0])
        print(self.__pr.preprocess_text(splta[0]))
        if (len(ststr) > 0 and tstr.count('?') > 0):
            if(self.__mpred.predict(text, self.__mapa.multymapa,
                                    './models/multy/multyclassmodel.h5',
                                    './tokenizers/multy/multyclasstokenizer.pickle') == "Дело"):
                bot.boto.send_message(
                    self.__message.chat.id, "Я в порядке", parse_mode='html')

                self.__set_null()
                self.__b_flag = 1
                self.__qu_flag = 1
                self.__mtext = tstr

            elif(self.__mpred.predict(text, self.__mapa.multymapa,
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

                self.__set_null()
                self.__q__non_flag = 1
                self.__qu_flag = 1
                self.__mtext = tstr
        elif(splta[0] in Cdict.values()):

            if(self.__bpred.predict(text, self.__mapa.commandmapa,
                                    './models/binary/commandmodel.h5',
                                    './tokenizers/binary/thtokenizer.pickle',
                                    'command') == "Команда"):
                self.__set_null()
                print("command")
                command = Commands.Command(bot.boto, self.__message )

                command.commandanalyse(tstr)

                self.__command_flag = command.command_flag
            else:
                bot.boto.send_message(
                    self.__message.chat.id, "Похоже на команду но я не уверена.",
                    parse_mode='html')

            self.__mtext = tstr
        elif(self.__bpred.predict(text, self.__mapa.himapa,
                                  './models/binary/himodel.h5',
                                  './tokenizers/binary/hitokenizer.pickle',
                                  '') == "Приветствие"):

            ra = bot.Answers.RandomAnswer()
            bot.boto.send_message(
                self.__message.chat.id, ra.answer(), parse_mode='html')

            self.__set_null()
            self.__hi_flag = 1
            self.__mtext = tstr

        elif(self.__bpred.predict(text, self.__mapa.thmapa,
                                  './models/binary/thmodel.h5',
                                  './tokenizers/binary/thtokenizer.pickle',
                                  '') == "Благодарность"):

            bot.boto.send_message(self.__message.chat.id, "Не за что",
                                  parse_mode='html')

            self.__set_null()
            self.__th_flag = 1
            self.__mtext = tstr
        else:

            if(self.__mpred.predict(text, self.__mapa.multymapa, './models/multy/multyclassmodel.h5',
                                    './tokenizers/multy/multyclasstokenizer.pickle') == "Дело"):
                bot.boto.send_message(
                    self.__message.chat.id, "Утверждение про дела", parse_mode='html')
                
                self.__set_null()
                self.__b_flag = 1
                self.__mtext = tstr

            elif(self.__mpred.predict(text, self.__mapa.multymapa, './models/multy/multyclassmodel.h5',
                                      './tokenizers/multy/multyclasstokenizer.pickle') == "Погода"):
                bot.boto.send_message(
                    self.__message.chat.id, "Утверждение про погоду", parse_mode='html')
                
                self.__set_null()
                self.__weater_flag = 1
                self.__mtext = tstr
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
        lowertext = self.__message.text.lower()
        print(lowertext)
        if(lowertext.count('миса') > 0 or lowertext.lower().count('misa') > 0):
            tstr = lowertext.replace("миса", '')
            ststr = tstr.replace("misa", '')
            text.append(ststr)

            for txt in text:
                data = {'text': txt, 'agenda': ''}
                df = bot.pd.DataFrame()
                new_row = bot.pd.Series(data)
                df = df.append(new_row, ignore_index=True)
                #print(df)
                df.to_sql('validset', con= self._engine, schema='public',
                          index=False, if_exists='append')
            self.__neurodesc(text, ststr)
          #  try:

         #  except:
         #       bot.boto.send_message(
          #          self.__message.chat.id, 'А?', parse_mode='html')
        elif(self.__message.text == "👍" and self.__hi_flag == 1):
            self.__ad.add(self.__mtext, 'recognized_hi',
                             "Приветствие", 'agenda', 'hi', 1)
            self.__be.hievaluate()
            self.__set_null()
        elif(self.__message.text == "👎" and self.__hi_flag == 1):
            self.ad.add(self.__mtext, 'recognized_hi',
                             "Не приветствие", 'agenda', 'hi', 0)
            self.__be.hievaluate()
            self.__set_null()
        elif(self.__message.text == "Вопрос без класса" and self.__qu_flag == 1):

            self.__ad.add(self.__mtext, 'recognized_multyclass',
                             "Нет классификации", 'agenda', 'questionclass', 0)
            self.__ad.quadd(self.__mtext, 'recognized_qu',
                               "Вопрос", 1)

            self.__me.multyclassevaluate()
            self.__set_null()
        elif(self.__message.text == "Не вопрос" and self.__qu_flag == 1):
            self.__ad.add(self.__mtext, 'recognized_multyclass',
                             "Нет классификации", 'agenda', 'questionclass', 0)
            self.__ad.quadd(self.__mtext, 'recognized_qu',
                               "Не вопрос", 0)
            self.__bt.quevaluate()

            bot.boto.send_message(
                self.__message.chat.id, "Запомнила", parse_mode='html')

            self.__set_null()
        elif(self.__message.text == "Погода" and self.__qu_flag == 1):
            self.__ad.add(self.__mtext, 'recognized_multyclass',
                             "Погода", 'agenda', 'questionclass', 1)
            self.__ad.quadd(self.__mtext, 'recognized_qu',
                               "Вопрос", 1)

            self.__me.multyclassevaluate()

            self.__set_null()
        elif(self.__message.text == "Дело" and self.__qu_flag == 1):
            self.__ad.add(self.__mtext, 'recognized_multyclass',
                             "Дело", 'agenda', 'questionclass', 1)
            self.__ad.quadd(self.__mtext, 'recognized_qu',
                               "Вопрос", 1)

            self.__me.multyclassevaluate()

            self.__bt.quevaluate()
            self.__set_null()
        elif(self.__message.text == "👍" and self.__command_flag == 1):
            self.__ad.commandadd(self.__mtext,
                                    'recognized_command',
                                    "Команда", 1)
            self.__bt.commandevaluate()
            self.__set_null()
        elif(self.__message.text == "👎" and self.__command_flag == 1):
            self.__ad.commandadd(self.__mtext, 'recognized_command',
                                    "Не команда", 0)
            self.__bt.commandevaluate()
            self.__set_null()
        elif(self.__message.text == "👍" and self.__th_flag == 1):
            self.__ad.add(
                self.__mtext, 'recognized_th',
                "Благодарность", 'agenda', 'thanks', 1)
            self.__set_null()
        elif(self.__message.text == "👎" and self.__th_flag == 1):
            self.__ad.add(self.__mtext, 'recognized_th',
                             "Не благодарность", 'agenda', 'thanks', 0)
            self.__bt.thevaluate()
            self.__set_null()
        elif(self.__message.text == "👍" and self.__non_flag == 1):
            self.__ad.add(
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
        text = []

class TestMonitor(MessageMonitor):

    inputtext = ""
    
    __bpred = bot.Predictors.Binary()
    __mpred = bot.Predictors.Multy()
    __qpr = bot.Models.TextPreprocessers.QuestionPreprocessing()
    __cpr = bot.Models.TextPreprocessers.CommandPreprocessing()
    __pr = bot.Models.TextPreprocessers.CommonPreprocessing()
    
    def __init__(self):
        self.__engine = super()._engine
        self.__conn = super()._conn


    def __insert_to_validset_lablel(self, txt, insert):
        
        data = {'text': txt,'agenda': insert}
        df = bot.pd.DataFrame()
        new_row = bot.pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql('markedvalidset', con=self.__engine, schema='public',
                          index=False, if_exists='append')
    
    def __neurodesc(self, text, tstr):

        df = bot.pd.read_sql('SELECT text FROM commands', self.__engine)
        Cdict = df['text'].to_dict()

        ststr = self.__qpr.reversepreprocess_text(tstr)
        a = self.__cpr.preprocess_text(text[0])
        splta = a.split()
     #   print("splta = ", splta[0])
        if (len(ststr) > 0 and tstr.count('?') > 0):
            if(self.__mpred.predict(text, bot.mapa.multymapa,
                                    './models/multy/multyclassmodel.h5',
                                    './tokenizers/multy/multyclasstokenizer.pickle') == "Дело"):
                insert = "Вопрос про дело"
                self.__insert_to_validset_lablel(tstr,insert)


            elif(self.__mpred.predict(text, bot.mapa.multymapa,
                                      './models/multy/multyclassmodel.h5',
                                      './tokenizers/multy/multyclasstokenizer.pickle') == "Погода"):
                
                insert = "Вопрос про погоду"
                self.__insert_to_validset_lablel(tstr,insert)

            else:
                
                insert = "Вопрос без классификации"
                self.__insert_to_validset_lablel(tstr,insert)

        elif(splta[0] in Cdict.values()):

            if(self.__bpred.predict(text, bot.mapa.commandmapa,
                                    './models/binary/commandmodel.h5',
                                    './tokenizers/binary/thtokenizer.pickle',
                                    'command') == "Команда"):
                insert = "Команда"
                self.__insert_to_validset_lablel(tstr,insert)

                
            else:
                
                insert = "Похоже на команду"
                self.__insert_to_validset_lablel(tstr,insert)
                self.__mtext = tstr


        elif(self.__bpred.predict(text, bot.mapa.himapa,
                                  './models/binary/himodel.h5',
                                  './tokenizers/binary/hitokenizer.pickle',
                                  '') == "Приветствие"):

            ra = bot.Answers.RandomAnswer()
            insert = "Приветствие"
            self.__insert_to_validset_lablel(tstr,insert)
            self.__mtext = tstr

        elif(self.__bpred.predict(text, bot.mapa.thmapa,
                                  './models/binary/thmodel.h5',
                                  './tokenizers/binary/thtokenizer.pickle',
                                  '') == "Благодарность"):
            
            insert = "Благодарность"
            self.__insert_to_validset_lablel(tstr,insert)
            self.__mtext = tstr
        else:

            if(self.__mpred.predict(text, bot.mapa.multymapa, './models/multy/multyclassmodel.h5',
                                    './tokenizers/multy/multyclasstokenizer.pickle') == "Дело"):

                insert = "Дело"
                self.__insert_to_validset_lablel(tstr,insert)
                self.__mtext = tstr
                
            elif(self.__mpred.predict(text, bot.mapa.multymapa, './models/multy/multyclassmodel.h5',
                                      './tokenizers/multy/multyclasstokenizer.pickle') == "Погода"):
                insert = "Погода"
                self.__insert_to_validset_lablel(tstr,insert)
                self.__mtext = tstr
            else:
                insert = "Нет классификации"
                self.__insert_to_validset_lablel(tstr,insert)
                self.__mtext = tstr

    def monitor(self):
        
        df = bot.pd.read_sql('SELECT * FROM validset', self.__conn)


        inptext = df['text']
        text = []
        
        for txt in inptext:

            tstr = txt.replace("миса", '')
            ststr = tstr.replace("misa", '')
            text.append(ststr)
        #    print(ststr)
            self.__neurodesc(text, ststr)
            text = []

