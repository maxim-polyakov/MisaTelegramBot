from sympy import *
from NLP import TextPreprocessers

class Calculator:
    
    def __init__(self):
        pass
    
    def find(self):
        pass
    
    
class SympyCalculator(Calculator):
    
    __pr = TextPreprocessers.QuestionPreprocessing()
    def __init__(self):
        pass
    
    def deravative(self, boto, message, inptmes, dx):
        
        
        inp = self.__pr.preprocess_text(dx)
        x = Symbol(inp[0])
        print(x)
        y = sympify(str(inptmes))
        yprime = y.diff(x)
        output = str(yprime).replace('**','^')
        boto.send_message(message.chat.id, output, parse_mode='html')