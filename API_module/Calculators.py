from sympy import *
from NLP import TextPreprocessers

class Calculator:
    
    def __init__(self):
        pass
    
    def find(self):
        pass
    
    
class WolframCalculator(Calculator):
    
    __pr = TextPreprocessers.CommonPreprocessing()
    def __init__(self):
        pass
    
    
    def deravative(self, boto, message, inptmes):
        inp = self.__pr.preprocess_text(inptmes)
        x = Symbol(inp)
       # y = 