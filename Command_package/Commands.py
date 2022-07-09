import NLP_package
from NLP_package import TextPreprocessers
#import pyTelegramBotAPI
from API_package import Finders as APIFind
from API_package import Calculators
import psycopg2

class Command:

    command_flag = 0

    __pred = TextPreprocessers.Preprocessing()
    __pr = TextPreprocessers.CommonPreprocessing()
    __cpr = TextPreprocessers.CommandPreprocessing()


    def __init__(self, boto, message):
        self.boto= boto
        self.message = message

    def __fas(self):

        inpt = self.message.text.split(' ')

        self.boto.send_message(self.message.chat.id, inpt[2] + " - пидор.", parse_mode='html')

    def __insidefunction(self,inpt):
        c = Calculators.SympyCalculator()
        if self.preprocess_text(inpt[2]) == 'производная':
            print(inpt[3])
            c.deravative(self.boto, self.message, inpt[3], inpt[4])
        elif self.preprocess_text(inpt[2]) == 'интеграл':
            c.integrate(self.boto, self.message, inpt[3], inpt[4])

    def commandsdesition(self, tstr):

        global command_flag

        preinpt = self.message.text.split('->')

        strr = self.__pred.preprocess_text(preinpt[0])
        inpt = strr.split(' ')
        print(inpt)
        if (self.__pr.preprocess_text(inpt[1]) == 'атаковать' or
                self.__pr.preprocess_text(inpt[1]) == 'фас' or
                self.__pr.preprocess_text(inpt[1]) == 'пиздануть'):
            self.__fas()
            self.command_flag = 1

        elif ((self.__pr.preprocess_text(inpt[1]) == 'поссчитать')):
            self.__insidefunction(self.__pr,self.boto,self.message,inpt)

        elif self.__pr.preprocess_text(inpt[1]) == 'находить':
            if self.__pr.preprocess_text(inpt[2]) == 'производная' or pr.preprocess_text(inpt[2]) == 'интеграл':

                self.__insidefunction(self.__pr,self.boto,self.message,inpt)
            else:

                tmp = self.__pr.preprocess_text(preinpt[1])
                apif = APIFind.WikiFinder()
                apif.find(self.boto, self.message, tmp)
                command_flag = 1

        else:
            self.send_message(self.message.chat.id, "Команда",
                              parse_mode='html')
            self.command_flag = 1



