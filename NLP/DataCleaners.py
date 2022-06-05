import NLP
from NLP import TextPreprocessers


class Cleaner:
    def __init__(self):
        pass
    
    def clean(self):
        pass
    
class CommonCleaner(Cleaner):
    def __init__(self):
        pass
    
    def clean(self, filename, string):
        pr = TextPreprocessers.CommonPreprocessing()
        train = NLP.pd.read_excel(filename)
        train.text = train.text.astype(str)
        df = NLP.pd.concat([train])
        df['text'] = df['text'].apply(pr.preprocess_text)
        train = df[~df[string].isna()]
        train[string] = train[string].astype(int)
        train.to_excel(filename, index=False)

class QuestionCleaner(Cleaner):
    def __init__(self):
        pass
    
    def clean(self, filename):
        pr = TextPreprocessers.QuestionPreprocessing()
        train = NLP.pd.read_excel(filename)
        train.text = train.text.astype(str)
        df = NLP.pd.concat([train])
        df['text'] = df['text'].apply(pr.preprocess_text)
        train = df[~df['question'].isna()]
        train['question'] = train['question'].astype(int)
        train.to_excel(filename, index=False)
        
def CommandCleaner(Cleaner):
    def __init__(self):
        pass
    
    def clean(self, filename):
        pr = TextPreprocessers.CommandPreprocessing()
        train = NLP.pd.read_excel(filename)
        train.text = train.text.astype(str)
        df = NLP.pd.concat([train])
        df['text'] = df['text'].apply(pr.preprocess_text)
        train = df[~df['command'].isna()]
        train['command'] = train['command'].astype(int)
        train.to_excel(filename, index=False)
