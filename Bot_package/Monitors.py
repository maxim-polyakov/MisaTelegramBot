import Bot_package

class Monitor:

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

    __bpred = Bot_package.bot.Predictors.Binary()
    __nnpred = Bot_package.bot.Predictors.NonNeuro()
    __mpred = Bot_package.bot.Predictors.Multy()
    __qpr = Bot_package.TextPreprocessers.QuestionPreprocessing()
    __cpr = Bot_package.TextPreprocessers.CommandPreprocessing()
    __pr = Bot_package.TextPreprocessers.CommonPreprocessing()
    
    _engine = Bot_package.create_engine(
                    'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
    _conn = Bot_package.psycopg2.connect(
        "dbname=postgres user=postgres password=postgres")

    __ad = Bot_package.Subfunctions.Adder()
    __bt = Bot_package.Bototrainers.Train()
    __mt = Bot_package.Bototrainers.Multytrain()
    __be = Bot_package.Botoevaluaters.Binaryevaluate()
    __me = Bot_package.Botoevaluaters.Multyevaluate()
    __mapa = Bot_package.bot.Mapas.Mapa()

    __emotion = ""

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

    def __emotionsrecognition(self,text):

            self.__emotion = self.__mpred.predict(text, self.__mapa.emotionsmapa,
                                   './models/multy/emotionsmodel.h5',
                                   './tokenizers/multy/emotionstokenizer.pickle')

    def __checkcommands(self, ststr):
        df = Bot_package.bot.pd.read_sql('SELECT text FROM commands', self._conn)
        Cdict = df['text'].to_dict()
        for cdictvalue in Cdict.values():
            if(cdictvalue in ststr):
                return True
        return False

    def __neurodesc(self, text, tstr):

        self.__emotionsrecognition(text)

        if (tstr.count('?') > 0):
            if (self.__mpred.predict(text, self.__mapa.multymapa,
                                     './models/multy/multyclassmodel.h5',
                                     './tokenizers/multy/multyclasstokenizer.pickle') == "????????"):
                Bot_package.bot.boto.send_message(
                    self.__message.chat.id, "?? ?? ?????????????? " + + self.__emotion, parse_mode='html')

                self.__set_null()
                self.__b_flag = 1
                self.__qu_flag = 1
                self.__mtext = tstr
            elif (self.__mpred.predict(text, self.__mapa.multymapa,
                                       './models/multy/multyclassmodel.h5',
                                       './tokenizers/multy/multyclasstokenizer.pickle') == "????????????"):
                Bot_package.bot.boto.send_message(
                    self.__message.chat.id, "???????????? ???????? " + self.__emotion, parse_mode='html')

                self.__set_null()
                self.__weater_flag = 1
                self.__qu_flag = 1
                self.__mtext = tstr

            else:
                Bot_package.bot.boto.send_message(
                    self.__message.chat.id, "???????????? ?????? ?????????????????????????? " + self.__emotion,
                    parse_mode='html')

                self.__set_null()
                self.__q__non_flag = 1
                self.__qu_flag = 1
                self.__mtext = tstr
        elif (self.__checkcommands(tstr)):

            if (self.__bpred.predict(text, self.__mapa.commandmapa,
                                     './models/binary/commandmodel.h5',
                                     './tokenizers/binary/thtokenizer.pickle',
                                     'command') == "??????????????"):
                self.__set_null()
                command = Bot_package.Commands.Command(Bot_package.bot.boto, self.__message)

                command.commandanalyse(tstr)

                self.__command_flag = command.command_flag
            else:
                Bot_package.bot.boto.send_message(
                    self.__message.chat.id, "???????????? ???? ?????????????? ???? ?? ???? ??????????????. " + self.__emotion,
                    parse_mode='html')

            self.__mtext = tstr
        elif (self.__bpred.predict(text, self.__mapa.himapa,
                                   './models/binary/himodel.h5',
                                   './tokenizers/binary/hitokenizer.pickle',
                                   '') == "??????????????????????"):

            ra = Bot_package.bot.Answers.RandomAnswer()
            Bot_package.bot.boto.send_message(
                self.__message.chat.id, ra.answer()[0] + self.__emotion, parse_mode='html')

            self.__set_null()
            self.__hi_flag = 1
            self.__mtext = tstr

        elif (self.__bpred.predict(text, self.__mapa.thmapa,
                                   './models/binary/thmodel.h5',
                                   './tokenizers/binary/thtokenizer.pickle',
                                   '') == "??????????????????????????"):

            Bot_package.bot.boto.send_message(self.__message.chat.id, "???? ???? ?????? " + self.__emotion,
                                              parse_mode='html')

            self.__set_null()
            self.__th_flag = 1
            self.__mtext = tstr
        else:
            if (self.__mpred.predict(text, self.__mapa.multymapa, './models/multy/multyclassmodel.h5',
                                     './tokenizers/multy/multyclasstokenizer.pickle') == "????????"):
                Bot_package.bot.boto.send_message(
                    self.__message.chat.id, "?????????????????????? ?????? ???????? " + self.__emotion, parse_mode='html')

                self.__set_null()
                self.__b_flag = 1
                self.__mtext = tstr

            elif (self.__mpred.predict(text, self.__mapa.multymapa, './models/multy/multyclassmodel.h5',
                                       './tokenizers/multy/multyclasstokenizer.pickle') == "????????????"):
                Bot_package.bot.boto.send_message(
                    self.__message.chat.id, "?????????????????????? ?????? ???????????? " + self.__emotion, parse_mode='html')

                self.__set_null()
                self.__weater_flag = 1
                self.__mtext = tstr
            else:
                Bot_package.bot.boto.send_message(
                    self.__message.chat.id, "?????? ?????????????????????????? " + self.__emotion,
                    parse_mode='html')

                self.__set_null()
                self.__non_flag = 1
                self.__mtext = tstr

    def __todb(self,lowertext):
        lowertext = lowertext.replace("???????? ", '').replace("misa ", '')
        text = []
        text.append(lowertext)
        for txt in text:
            data = {'text': txt, 'agenda': ''}
            df = Bot_package.bot.pd.DataFrame()
            new_row = Bot_package.bot.pd.Series(data)
            df = df.append(new_row, ignore_index=True)
            df.to_sql('validset', con=self._engine, schema='public',
                      index=False, if_exists='append')

    def monitor(self):

        text = []
        lowertext = self.__message.text.lower()
        self.__todb(lowertext)

        if(lowertext.count('????????') > 0 or lowertext.lower().count('misa') > 0):

            lowertext = lowertext.replace("???????? ", '').replace("misa ", '')
            text.append(lowertext)
            self.__neurodesc(text, lowertext)
          #  try:

          #  except:
          #      Bot_package.bot.boto.send_message(self.__message.chat.id, '???', parse_mode='html')
        elif(self.__message.text == "????" and self.__hi_flag == 1):
            self.__ad.add(self.__mtext, 'recognized_hi',
                             "??????????????????????", 'agenda', 'hi', 1)
            self.__be.hievaluate()
            self.__set_null()
        elif(self.__message.text == "????" and self.__hi_flag == 1):
            self.ad.add(self.__mtext, 'recognized_hi',
                             "???? ??????????????????????", 'agenda', 'hi', 0)
            self.__be.hievaluate()
            self.__set_null()
        elif(self.__message.text == "???????????? ?????? ????????????" and self.__qu_flag == 1):

            self.__ad.add(self.__mtext, 'recognized_multyclass',
                             "?????? ??????????????????????????", 'agenda', 'questionclass', 0)
            self.__ad.quadd(self.__mtext, 'recognized_qu',
                               "????????????", 1)

            self.__me.multyclassevaluate()
            self.__set_null()
        elif(self.__message.text == "???? ????????????" and self.__qu_flag == 1):
            self.__ad.add(self.__mtext, 'recognized_multyclass',
                             "?????? ??????????????????????????", 'agenda', 'questionclass', 0)
            self.__ad.quadd(self.__mtext, 'recognized_qu',
                               "???? ????????????", 0)
            self.__bt.quevaluate()

            Bot_package.bot.boto.send_message(
                self.__message.chat.id, "??????????????????", parse_mode='html')

            self.__set_null()
        elif(self.__message.text == "????????????" and self.__qu_flag == 1):
            self.__ad.add(self.__mtext, 'recognized_multyclass',
                             "????????????", 'agenda', 'questionclass', 1)
            self.__ad.quadd(self.__mtext, 'recognized_qu',
                               "????????????", 1)

            self.__me.multyclassevaluate()

            self.__set_null()
        elif(self.__message.text == "????????" and self.__qu_flag == 1):
            self.__ad.add(self.__mtext, 'recognized_multyclass',
                             "????????", 'agenda', 'questionclass', 1)
            self.__ad.quadd(self.__mtext, 'recognized_qu',
                               "????????????", 1)

            self.__me.multyclassevaluate()

            self.__bt.quevaluate()
            self.__set_null()
        elif(self.__message.text == "????" and self.__command_flag == 1):
            self.__ad.commandadd(self.__mtext,
                                    'recognized_command',
                                    "??????????????", 1)
            self.__bt.commandevaluate()
            self.__set_null()
        elif(self.__message.text == "????" and self.__command_flag == 1):
            self.__ad.commandadd(self.__mtext, 'recognized_command',
                                    "???? ??????????????", 0)
            self.__bt.commandevaluate()
            self.__set_null()
        elif(self.__message.text == "????" and self.__th_flag == 1):
            self.__ad.add(
                self.__mtext, 'recognized_th',
                "??????????????????????????", 'agenda', 'thanks', 1)
            self.__set_null()
        elif(self.__message.text == "????" and self.__th_flag == 1):
            self.__ad.add(self.__mtext, 'recognized_th',
                             "???? ??????????????????????????", 'agenda', 'thanks', 0)
            self.__bt.thevaluate()
            self.__set_null()
        elif(self.__message.text == "????" and self.__non_flag == 1):
            self.__ad.add(
                self.__mtext, 'non_recognized',
                "?????? ??????????????????????????", 'agenda', 'nonclass', 1)
            self.__set_null()
        elif(self.__message.text == "????" and self.__non_flag == 1):
            self.__set_null()
        elif(self.__message.text == "????"):
            Bot_package.bot.boto.send_message(self.__message.chat.id,
                                  "????", parse_mode='html')
        elif(self.__message.text == "????"):
            Bot_package.bot.boto.send_message(self.__message.chat.id,
                                  "????", parse_mode='html')
        text = []

class TestMonitor(MessageMonitor):

    inputtext = ""
    
    __bpred = Bot_package.Predictors.Binary()
    __mpred = Bot_package.Predictors.Multy()
    __qpr = Bot_package.TextPreprocessers.QuestionPreprocessing()
    __cpr = Bot_package.TextPreprocessers.CommandPreprocessing()
    __pr = Bot_package.TextPreprocessers.CommonPreprocessing()
    
    def __init__(self):
        self.__engine = super()._engine
        self.__conn = super()._conn


    def __insert_to_validset_lablel(self, txt, insert):
        
        data = {'text': txt,'agenda': insert}
        df = Bot_package.bot.pd.DataFrame()
        new_row = Bot_package.bot.pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql('markedvalidset', con=self.__engine, schema='public',
                          index=False, if_exists='append')
    
    def __neurodesc(self, text, tstr):

        df = Bot_package.bot.pd.read_sql('SELECT text FROM commands', self.__engine)
        Cdict = df['text'].to_dict()

        ststr = self.__qpr.reversepreprocess_text(tstr)
        a = self.__cpr.preprocess_text(text[0])
        splta = a.split()
     #   print("splta = ", splta[0])
        if (len(ststr) > 0 and tstr.count('?') > 0):
            if(self.__mpred.predict(text, Bot_package.bot.mapa.multymapa,
                                    './models/multy/multyclassmodel.h5',
                                    './tokenizers/multy/multyclasstokenizer.pickle') == "????????"):
                insert = "???????????? ?????? ????????"
                self.__insert_to_validset_lablel(tstr,insert)


            elif(self.__mpred.predict(text, Bot_package.bot.mapa.multymapa,
                                      './models/multy/multyclassmodel.h5',
                                      './tokenizers/multy/multyclasstokenizer.pickle') == "????????????"):
                
                insert = "???????????? ?????? ????????????"
                self.__insert_to_validset_lablel(tstr,insert)

            else:
                
                insert = "???????????? ?????? ??????????????????????????"
                self.__insert_to_validset_lablel(tstr,insert)

        elif(splta[0] in Cdict.values()):

            if(self.__bpred.predict(text, Bot_package.bot.mapa.commandmapa,
                                    './models/binary/commandmodel.h5',
                                    './tokenizers/binary/thtokenizer.pickle',
                                    'command') == "??????????????"):
                insert = "??????????????"
                self.__insert_to_validset_lablel(tstr,insert)

                
            else:
                
                insert = "???????????? ???? ??????????????"
                self.__insert_to_validset_lablel(tstr,insert)
                self.__mtext = tstr


        elif(self.__bpred.predict(text, Bot_package.bot.mapa.himapa,
                                  './models/binary/himodel.h5',
                                  './tokenizers/binary/hitokenizer.pickle',
                                  '') == "??????????????????????"):

            ra = Bot_package.bot.Answers.RandomAnswer()
            insert = "??????????????????????"
            self.__insert_to_validset_lablel(tstr,insert)
            self.__mtext = tstr

        elif(self.__bpred.predict(text, Bot_package.bot.mapa.thmapa,
                                  './models/binary/thmodel.h5',
                                  './tokenizers/binary/thtokenizer.pickle',
                                  '') == "??????????????????????????"):
            
            insert = "??????????????????????????"
            self.__insert_to_validset_lablel(tstr,insert)
            self.__mtext = tstr
        else:

            if(self.__mpred.predict(text, Bot_package.bot.mapa.multymapa, './models/multy/multyclassmodel.h5',
                                    './tokenizers/multy/multyclasstokenizer.pickle') == "????????"):

                insert = "????????"
                self.__insert_to_validset_lablel(tstr,insert)
                self.__mtext = tstr
                
            elif(self.__mpred.predict(text, Bot_package.bot.mapa.multymapa, './models/multy/multyclassmodel.h5',
                                      './tokenizers/multy/multyclasstokenizer.pickle') == "????????????"):
                insert = "????????????"
                self.__insert_to_validset_lablel(tstr,insert)
                self.__mtext = tstr
            else:
                insert = "?????? ??????????????????????????"
                self.__insert_to_validset_lablel(tstr,insert)
                self.__mtext = tstr

    def monitor(self):
        
        df = Bot_package.bot.pd.read_sql('SELECT * FROM validset', self.__conn)


        inptext = df['text']
        text = []
        
        for txt in inptext:

            tstr = txt.replace("????????", '')
            ststr = tstr.replace("misa", '')
            text.append(ststr)
        #    print(ststr)
            self.__neurodesc(text, ststr)
            text = []

