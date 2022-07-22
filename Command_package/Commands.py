import Command_package

class Command:

    command_flag = 0
    __pred = Command_package.TextPreprocessers.Preprocessing()
    __pr = Command_package.TextPreprocessers.CommonPreprocessing()
    __cpr = Command_package.TextPreprocessers.CommandPreprocessing()

    def __init__(self, boto, message):
        self.boto= boto
        self.message = message
    def __fas(self,Inputstr):
        Inputstr = Inputstr.replace("атакуй ", '').replace("пиздани ", '').replace("фас ", '')
     #   Inputstr = Inputstr.replace("фас ", '')
     #   Inputstr = Inputstr.replace("пиздани ", '')
        Inputstr = Inputstr.split(' ')
        self.boto.send_message(self.message.chat.id, Inputstr[0] + " - пидор.", parse_mode='html')
        self.command_flag = 1

    def __calculate(self, Inputstr):
        c = Command_package.Calculators.SympyCalculator()
        if Inputstr[0] == 'производная':
            c.deravative(self.boto, self.message, Inputstr[1], Inputstr[2])
        elif Inputstr[0] == 'интеграл':
            c.integrate(self.boto, self.message, Inputstr[1], Inputstr[2])
        self.command_flag = 1

    def __find(self,Inputstr):
        Inputstr = Inputstr.strip(' ').replace("найди ", '').replace("поссчитай ", '')
        tmp = self.__pred.preprocess_text(Inputstr)
        if (tmp.count('производная') > 0) or (tmp.count('интеграл') > 0):
            inptt = tmp.split(' ')
            self.__calculate(inptt)
        else:
            apif = Command_package.Finders.WikiFinder()
            apif.find(self.boto, self.message, Inputstr)
        self.command_flag = 1

    def __translate(self, Inputstr):
        Inputstr = Inputstr.strip(' ').replace("переведи ", '')
        tr = Command_package.Translators.GoogleTranslator("ru")
        if (Inputstr.count('данные') > 0):
            dataselect = 'SELECT * FROM ' + Inputstr[2]
            insertdtname = 'translated'
            tr.translatedt(dataselect, insertdtname)
        else:
            tr.translate(self.boto, self.message, Inputstr)
        self.command_flag = 1

    def __show(self, Inputstr):
        Inputstr = self.__pred.preprocess_text(Inputstr)
        Inputstr = Inputstr.replace("показывать ", '')
        Inputstr = Inputstr.strip(' ')
        Inputstr = Inputstr.split(' ')
        if (self.__pr.preprocess_text(Inputstr[0]) == 'данные'):
            dataselect = 'SELECT * FROM ' + Inputstr[1]
            recognizeddataselect = 'SELECT * FROM ' + "recognized_" + Inputstr[1]
            target = Inputstr[2]
            ds = Command_package.DataShowers.DataShower(self.boto, self.message, dataselect, recognizeddataselect)
            ds.showdata(target)
        self.command_flag = 1

    def commandanalyse(self, Inputstr):

        PreprocessedInputstr = self.__pred.preprocess_text(Inputstr)
        if (PreprocessedInputstr.count('атаковать')>0 or
                PreprocessedInputstr.count('фас') > 0 or
                PreprocessedInputstr.count('пиздануть') > 0):
            self.__fas(Inputstr)
        elif (PreprocessedInputstr.count('находить') > 0) or (PreprocessedInputstr.count('поссчитать') > 0):
            self.__find(Inputstr)
        elif (PreprocessedInputstr.count('перевести') > 0):
            self.__translate(Inputstr)
        elif (PreprocessedInputstr.count('показывать') > 0):
            self.__show(Inputstr)
        else:
            self.boto.send_message(self.message.chat.id, "Команда",
                              parse_mode='html')
            self.command_flag = 1



