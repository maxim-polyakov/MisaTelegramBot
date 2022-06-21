import rpa as r
import RPA_module
import bot

class Founder:
    
    def __init__(self):
        pass
    
    def find(self):
        pass
    
    
class WikiFounder(Founder):
    def __init__(self):
        pass
    
    def find(self, boto, message, inptmes):
        r.init(visual_automation = False, chrome_browser = True)
        r.url('https://ru.wikipedia.org/')
        r.type('//*[@name="search"]', inptmes + '[enter]')

        r.snap('//*[@class = "thumb tright"]', './RPA_module/fresults.jpg')

        boto.send_photo(message.chat.id, open('./RPA_module/fresults.jpg','rb'))
        boto.send_message(message.chat.id, r.read('p'),
                           parse_mode='html')
        r.close()
        