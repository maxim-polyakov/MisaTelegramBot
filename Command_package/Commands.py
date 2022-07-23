import Command_package

class Command:

    command_flag = 0
    __pred = Command_package.TextPreprocessers.Preprocessing()
    __pr = Command_package.TextPreprocessers.CommonPreprocessing()
    __cpr = Command_package.TextPreprocessers.CommandPreprocessing()
    __nothingflg = 0
    __cash = ''
    __conn = Command_package.psycopg2.connect(
        "dbname=postgres user=postgres password=postgres")

    __df = Command_package.pd.read_sql('SELECT text FROM commands', self.__conn)
    __Cdict = __df['text'].to_dict()
    def __init__(self, boto, message):
        self.boto= boto
        self.message = message

    def __fas(self,Inputstr):
        Inputstr = self.__pred.preprocess_text(Inputstr)
        Inputstr = Inputstr.replace("атакуй ", '').replace("пиздани ", '').replace("фас ", '')
        Inputarr = Inputstr.split(' ')
        self.boto.send_message(self.message.chat.id, Inputarr[0] + " - пидор.", parse_mode='html')
        self.command_flag = 1
        Inputstr = Inputstr.replace(Inputarr[0] + ' ', '')
        return Inputstr

    def __calculate(self, Inputstr):
        Inputarr = Inputstr.split(' ')
        c = Command_package.Calculators.SympyCalculator()
        if self.__pr.preprocess_text(Inputarr[0]) == 'производная':
            c.deravative(self.boto, self.message, Inputarr[1], Inputarr[2])
        elif self.__pr.preprocess_text(Inputarr[0]) == 'интеграл':
            c.integrate(self.boto, self.message, Inputarr[1], Inputarr[2])
        Inputstr = Inputstr.replace(Inputarr[1].rstrip(), '')
        Inputstr = Inputstr.replace(Inputarr[2], '').replace(Inputarr[0], '')
        Inputstr = Inputstr.strip(' ')
        self.command_flag = 1
        return Inputstr

    def __find(self,Inputstr):
        Inputstr = Inputstr.strip(' ').replace("найди ", '').replace("поссчитай ", '')
        tmp = self.__pr.preprocess_text(Inputstr)
        if (tmp.count('производная') > 0) or (tmp.count('интеграл') > 0):

            Inputstr = self.__calculate(Inputstr)
        else:
            apif = Command_package.Finders.WikiFinder()
            apif.find(self.boto, self.message, tmp)
        self.command_flag = 1
        return Inputstr

    def __translate(self, Inputstr):
        tmp = Inputstr.count('переведи данные')
        Inputstr = Inputstr.strip(' ').replace("переведи ", '')
        tr = Command_package.Translators.GoogleTranslator("ru")
        if (tmp > 0):
            dataselect = 'SELECT * FROM ' + Inputstr[2]
            insertdtname = 'translated'
            tr.translatedt(dataselect, insertdtname)
        else:

            tr.translate(self.boto, self.message, Inputstr)
        self.command_flag = 1

    def __show(self, Inputstr):
        Inputstr = self.__pred.preprocess_text(Inputstr)
        Inputstr = Inputstr.strip(' ').replace("покажи ", '')
        Inputarr = Inputstr.split(' ')
        if (self.__pr.preprocess_text(Inputarr[0]) == 'данные'):
            dataselect = 'SELECT * FROM ' + Inputarr[1]
            recognizeddataselect = 'SELECT * FROM ' + "recognized_" + Inputarr[1]
            target = Inputarr[2]
            ds = Command_package.DataShowers.DataShower(self.boto, self.message, dataselect, recognizeddataselect)
            ds.showdata(target)
        self.command_flag = 1

    def commandanalyse(self, Inputstr):

        if(Inputstr.count('.')>0):
            Insidestringarr = Inputstr.split('. ')

        Insidestringarr = Inputstr.split(', ')
        for idx in range(0,len(Insidestringarr)):
            PreprocessedInputstr = self.__pr.preprocess_text(Insidestringarr[idx])
            PreprocessedInsidestringarr = self.__pred.preprocess_text(Insidestringarr[idx])
            if (PreprocessedInputstr.count('атаковать')>0 or
                    PreprocessedInputstr.count('фас') > 0 or
                    PreprocessedInputstr.count('пиздануть') > 0):
                self.__fas(PreprocessedInsidestringarr)
                self.__cash = 'атаковать'
                self.__nothingflg = 1
            if (PreprocessedInputstr.count('находить') > 0) or (PreprocessedInputstr.count('поссчитать') > 0):
                    self.__find(PreprocessedInsidestringarr)
                    self.__cash = 'находить'
                    self.__nothingflg = 2
            if (PreprocessedInputstr.count('перевести') > 0):
                self.__translate(PreprocessedInsidestringarr)
                self.__cash = 'перевести'
                self.__nothingflg = 3
            if (PreprocessedInputstr.count('показывать') > 0):
                self.__show(PreprocessedInsidestringarr)
                self.__nothingflg = 4

            if(self.__nothingflg == 0):
                if(Insidestringarr[idx] in self.Cdict.values()):
                    self.boto.send_message(self.message.chat.id, "Команда", parse_mode='html')
                else:
                    self.boto.send_message(self.message.chat.id, "Не команда", parse_mode='html')
                    if(self.__cash == 'находить'):
                        self.__find(PreprocessedInsidestringarr)
                    elif(self.__cash == 'атаковать'):
                        self.__fas(PreprocessedInsidestringarr)
                    elif(self.__cash == 'перевести'):
                        self.__translate(PreprocessedInsidestringarr)
            self.__nothingflg = 0

        self.command_flag = 1



