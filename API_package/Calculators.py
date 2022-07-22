import API_package

class Calculator:
    
    def __init__(self):
        pass
    
    def find(self):
        pass
    
    
class SympyCalculator(Calculator):
    
    __pr = API_package.tp.QuestionPreprocessing()
    def __init__(self):
        pass
    
    def deravative(self, boto, message, inptmes, dx):
        
        inp = self.__pr.preprocess_text(dx)
        x = API_package.Symbol(inp[0])
        print(x)
        y = API_package.sympify(str(inptmes))
        yprime = y.diff(x)
        output = str(yprime).replace('**','^')
        boto.send_message(message.chat.id, output, parse_mode='html')
    
    def integrate(self, boto, message, inptmes, dx):
        
        inp = self.__pr.preprocess_text(dx)
        x = API_package.Symbol(inp[0])
        print(x)
        y = API_package.sympify(str(inptmes))
        yprime = y.integrate(x)
        output = str(yprime).replace('**','^')
        boto.send_message(message.chat.id, output, parse_mode='html')