import pandas as pd
import NLP

def add(text,file,string):
    read = pd.read_excel(file)
    data =  {'text': NLP.libraries.preprocess_text(text),'agenda': string, 'hi': 1}
    df = pd.DataFrame(read)
    new_row = pd.Series(data)
    df = df.append(new_row, ignore_index=True)
    df.to_excel(file,index=False)
    
def quadd(text,file,string):
    read = pd.read_excel(file)
    data =  {'text': NLP.libraries.specialpreprocess_text(text),'agenda': string, 'hi': 1}
    df = pd.DataFrame(read)
    new_row = pd.Series(data)
    df = df.append(new_row, ignore_index=True)
    df.to_excel(file,index=False)
    