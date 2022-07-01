import API_module

class Finder:
    
    def __init__(self):
        pass
    
    def find(self):
        pass
    
    
class WikiFinder(Finder):
    def __init__(self):
        pass
    
    def find(self, boto, message, inptmes):
        API_module.w.set_lang("ru")
        
        boto.send_message(message.chat.id, API_module.w.summary(inptmes),
                           parse_mode='html')
        
        for i in range(0,6):
            try:
                boto.send_photo(message.chat.id, API_module.w.page(inptmes).images[i],
                                parse_mode='html')
            except:
                pass