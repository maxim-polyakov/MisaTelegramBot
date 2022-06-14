import rpa as r
import RPA_module
import codecs

class Calculator:
    
    def __init__(self):
        pass
    
    def find(self):
        pass
    
    
class WolframCalculator(Calculator):
    def __init__(self):
        pass
    
    def deravative(self, boto, message, inptmes):
        r.init(visual_automation = False, chrome_browser = True)
        r.url('https://www.wolframalpha.com/')
        r.type('//*[@class="_2Ejx"]', 'd('+ inptmes + ')' + '/dx' + '[enter]')
        r.snap('//*[@class = "_3fR4"]', './RPA_module/results.jpg')
        
        r.close()
        boto.send_photo(message.chat.id, open('./RPA_module/results.jpg','rb'))
        