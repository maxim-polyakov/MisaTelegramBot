import Command_package

class Command:

    command_flag = 0
    __pred = Command_package.TextPreprocessers.Preprocessing()
    __pr = Command_package.TextPreprocessers.CommonPreprocessing()
    __cpr = Command_package.TextPreprocessers.CommandPreprocessing()

    def __init__(self, boto, message):
        self.boto= boto
        self.message = message
    def __fas(self):

        inpt = self.message.text.split(' ')

        self.boto.send_message(self.message.chat.id, inpt[2] + " - пидор.", parse_mode='html')

        self.command_flag = 1
    def __insidefunction(self, inpt):
        c = Command_package.Calculators.SympyCalculator()
        if inpt[0] == 'производная':
            c.deravative(self.boto, self.message, inpt[1], inpt[2])
        elif inpt[0] == 'интеграл':
            c.integrate(self.boto, self.message, inpt[1], inpt[2])
        self.command_flag = 1
    def __find(self,inpt):
        print(inpt)
        tmp = self.__pred.preprocess_text(inpt)
        print(tmp.count('производная'))
        if (tmp.count('производная') > 0) or (tmp.count('интеграл') > 0):
            inptt = tmp.split(' ')
            self.__insidefunction(inptt)
        else:
            apif = Command_package.Finders.WikiFinder()
            apif.find(self.boto, self.message, inpt)
        self.command_flag = 1
    def __translate(self,strr):
        tr = Command_package.Translators.GoogleTranslator("ru")
        print(strr)
        if (strr.count('данные') > 0):
            dataselect = 'SELECT * FROM ' + inpt[2]
            insertdtname = 'translated'
            tr.translatedt(dataselect, insertdtname)
        else:
            tr.translate(self.boto, self.message, strr)
        self.command_flag = 1
    def __show(self, inpt):
        print(inpt)
        inpt = inpt.split(' ')
        if (self.__pr.preprocess_text(inpt[0]) == 'данные'):
            dataselect = 'SELECT * FROM ' + inpt[1]
            recognizeddataselect = 'SELECT * FROM ' + "recognized_" + inpt[1]
            target = inpt[2]
            ds = Command_package.DataShowers.DataShower(self.boto, self.message, dataselect, recognizeddataselect)
            ds.showdata(target)
        self.command_flag = 1
    def commandanalyse(self, tstr):
        preinpt = tstr.split('->')

        strr = self.__pred.preprocess_text(tstr)
        print("strr = ",strr)
        inpt = strr.split(' ')
        if (strr.count('атаковать')>0 or
                strr.count('фас') > 0 or
                strr.count('пиздануть') > 0):
            strr = strr.replace("атаковать ", '')
            strr = tstr.replace("фас ")
            strr = fstr.replace("пиздануть ")
            self.__fas()
        elif (strr.count('поссчитать') > 0):
            strr = strr.replace("поссчитать ", '')
            strr = strr.strip(' ')
            self.__find(strr)
        elif (strr.count('находить') > 0):

            strr = strr.replace("находить ", '')
            strr = strr.strip(' ')
            self.__find(strr)
        elif (strr.count('перевести') > 0):
            strr = strr.replace("перевести ", '')
            strr = strr.strip(' ')
            self.__translate(strr)
        elif (strr.count('показывать') > 0):
            strr = strr.replace("показывать ", '')
            strr = strr.strip(' ')
            print(strr)
            self.__show(strr)
        else:
            self.boto.send_message(self.message.chat.id, "Команда",
                              parse_mode='html')
            self.command_flag = 1



