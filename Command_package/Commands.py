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
        if self.__pr.preprocess_text(inpt[2]) == 'производная':
            print(inpt[3])
            c.deravative(self.boto, self.message, inpt[3], inpt[4])
        elif self.preprocess_text(inpt[2]) == 'интеграл':
            c.integrate(self.boto, self.message, inpt[3], inpt[4])
        self.command_flag = 1
    def __find(self,preinpt, inpt):
        if self.__pr.preprocess_text(inpt[2]) == 'производная' or self.__pr.preprocess_text(inpt[2]) == 'интеграл':

            self.__insidefunction(inpt)
        else:

            tmp = self.__pr.preprocess_text(preinpt[1])
            apif = Command_package.Finders.WikiFinder()
            apif.find(self.boto, self.message, tmp)

        self.command_flag = 1
    def __translate(self,preinpt,inpt):

        tr = Command_package.Translators.GoogleTranslator("ru")
        if (self.__pr.preprocess_text(inpt[2]) == 'данные'):
            dataselect = 'SELECT * FROM ' + inpt[3]
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

        preinpt = self.message.text.split('->')

        strr = self.__pred.preprocess_text(preinpt[0])
        inpt = strr.split(' ')
        print(self.__pr.preprocess_text(inpt[1]))
        if (self.__pr.preprocess_text(inpt[1]) == 'атаковать' or
                self.__pr.preprocess_text(inpt[1]) == 'фас' or
                self.__pr.preprocess_text(inpt[1]) == 'пиздануть'):
            self.__fas()
        elif ((self.__pr.preprocess_text(inpt[1]) == 'поссчитать')):
            self.__insidefunction(inpt)
        elif self.__pr.preprocess_text(inpt[1]) == 'находить':
            self.__find(preinpt, inpt)
        elif self.__pr.preprocess_text(inpt[1]) == 'перевести':
            self.__translate(preinpt,inpt)
        elif self.__pr.preprocess_text(inpt[1]) == 'показывать':
            self.__show(preinpt,inpt)
        else:
            self.boto.send_message(self.message.chat.id, "Команда",
                              parse_mode='html')
            self.command_flag = 1



