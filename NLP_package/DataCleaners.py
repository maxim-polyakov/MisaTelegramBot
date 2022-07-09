import NLP_package
from NLP_package import TextPreprocessers


class Cleaner:
    def __init__(self):
        pass
    
    def clean(self):
        pass
    
    
class CommonCleaner(Cleaner):
    
    __pr = TextPreprocessers.CommonPreprocessing()
    
    def __init__(self):
        pass
    
    def __init__(self, type_doc):
        self.type_doc = type_doc
    
    def clean(self, filename, string):
        
        if(self.type_doc == "csv"):
            train = NLP_package.pd.read_csv(filename, encoding="utf-8")
        else:
            train = NLP_package.pd.read_excel(filename)
        
        train.text = train.text.astype(str)
        df = NLP_package.pd.concat([train])
        df['text'] = df['text'].apply(self.__pr.preprocess_text)
        train = df[~df[string].isna()]
        train[string] = train[string].astype(int)
        train.to_csv(filename, index=False)

class QuestionCleaner(Cleaner):
    
    __pr = TextPreprocessers.QuestionPreprocessing()
    
    def __init__(self):
        pass  
    
    def __init__(self, type_doc):
        self.type_doc = type_doc
    
    def clean(self, filename):
        
        if(self.type_doc == "csv"):
            
            train = NLP_package.pd.read_csv(filename, encoding="utf-8")
        else:
            train = NLP_package.pd.read_excel(filename)
        
        train.text = train.text.astype(str)
        df = NLP_package.pd.concat([train])
        df['text'] = df['text'].apply(self.__pr.preprocess_text)
        train = df[~df['question'].isna()]
        train['question'] = train['question'].astype(int)
        train.to_excel(filename, index=False)
        
class CommandCleaner(Cleaner):
    
    __pr = TextPreprocessers.CommandPreprocessing()
    
    def __init__(self):
        pass
    
    def __init__(self, type_doc):
        self.type_doc = type_doc
    
    def clean(self, filename):
        
        if(self.type_doc == "csv"):
            
            train = NLP_package.pd.read_csv(filename, encoding="utf-8")
        else:
            train = NLP_package.pd.read_excel(filename)
            
        train.text = train.text.astype(str)
        df = NLP_package.pd.concat([train])
        df['text'] = df['text'].apply(self.__pr.preprocess_text)
        train = df[~df['command'].isna()]
        train['command'] = train['command'].astype(int)
        train.to_excel(filename, index=False)
