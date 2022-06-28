import wikipedia as w

class Finder:
    
    def __init__(self):
        pass
    
    def find(self):
        pass
    
    
class WikiFinder(Finder):
    def __init__(self):
        pass
    
    def find(self, boto, message, inptmes):
        w.set_lang("ru")
        
        boto.send_message(message.chat.id, w.summary(inptmes),
                           parse_mode='html')
        
        for i in range(0,6):
            try:
                boto.send_photo(message.chat.id, w.page(inptmes).images[i],
                                parse_mode='html')
            except:
                pass