import rpa as r
import RPA_module
import bot

class Calculator:
    
    def __init__(self):
        pass
    
    def find(self):
        pass
    
    
class WolframCalculator(Calculator):
    def __init__(self):
        pass
    
    def deravative(self, boto, message, reply_markup, inptmes):
        r.init(visual_automation = False, chrome_browser = True)
        r.url('https://www.wolframalpha.com/')
        r.type('//*[@class="_2Ejx"]', 'd('+ inptmes + ')' + '/dx' + '[enter]')
        r.snap('//*[@class = "_3fR4"]', 'results.png')
        r.close()
        