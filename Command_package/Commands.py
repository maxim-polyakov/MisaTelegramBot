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
        if self.__pr.preprocess_text(inpt[0]) == 'производная':
            print(inpt[3])
            c.deravative(self.boto, self.message, inpt[1], inpt[2])
        elif self.__pr.preprocess_text(inpt[0]) == 'интеграл':
            c.integrate(self.boto, self.message, inpt[1], inpt[2])
        self.command_flag = 1
    def __find(self,inpt):

        if (inpt.count('производная') > 0) or (inpt.count('интеграл') > 0):
            inptt = inpt.split(' ')
            print(inptt)
            self.__insidefunction(inptt)
        else:


            apif = Command_package.Finders.WikiFinder()
            apif.find(self.boto, self.message, inpt)

        self.command_flag = 1
    def __translate(self,preinpt,inpt):

        tr = Command_package.Translators.GoogleTranslator("ru")
        if (self.__pr.preprocess_text(inpt[1]) == 'данные'):
            dataselect = 'SELECT * FROM ' + inpt[2]
            insertdtname = 'translated'
            tr.translatedt(dataselect, insertdtname)
        else:
            tr.translate(self.boto, self.message, preinpt[1])
        self.command_flag = 1
    def __show(self,inpt):
        if (self.__pr.preprocess_text(inpt[2]) == 'данные'):
            dataselect = 'SELECT * FROM ' + inpt[3]
            recognizeddataselect = 'SELECT * FROM ' + "recognized_" + inpt[3]
            target = inpt[4]
            ds = Command_package.DataShowers.DataShower(self.boto, self.message, dataselect, recognizeddataselect)
            ds.showdata(target)
        self.command_flag = 1
    def commandanalyse(self, tstr):
      #  print(tstr)
        preinpt = tstr.split('->')

        strr = self.__pr.preprocess_text(tstr)
        print("strr = ",strr)
        inpt = strr.split(' ')
       # print(inpt)
       # print(self.__pr.preprocess_text(inpt[0]))
        if (strr.count('атаковать')>0 or
                strr.count('фас') > 0 or
                strr.count('пиздануть') > 0):
            tstr = strr.replace("атаковать ", '')
            fstr = tstr.replace("фас ")
            sstr = fstr.replace("пиздануть ")


            self.__fas()
        elif (strr.count('поссчитать') > 0):
            self.__insidefunction(inpt)
        elif (strr.count('находить') > 0):

            strr = tstr.replace("найди ", '')
            fstr = strr.strip(' ')
            self.__find(fstr)
        elif (strr.count('перевести') > 0):
            self.__translate(preinpt,inpt)
        elif (strr.count('показывать') > 0):
            self.__show(preinpt,inpt)
        else:
            self.boto.send_message(self.message.chat.id, "Команда",
                              parse_mode='html')
            self.command_flag = 1



