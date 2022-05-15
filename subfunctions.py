import pandas as pd
import NLP


def add(text, file, string, agenda, classification, classtype):
    read = pd.read_excel(file)
    data = {'text': NLP.libraries.preprocess_text(
        text), agenda: string, classification: classtype}
    df = pd.DataFrame(read)
    new_row = pd.Series(data)
    df = df.append(new_row, ignore_index=True)
    df.to_excel(file, index=False)


def quadd(text, file, string, isqu):
    read = pd.read_excel(file)
    data = {'text': NLP.libraries.specialpreprocess_text(
        text), 'agenda': string, 'question': isqu}
    df = pd.DataFrame(read)
    new_row = pd.Series(data)
    df = df.append(new_row, ignore_index=True)
    df.to_excel(file, index=False)
    
def commandadd(text, file, string, isqu):
    read = pd.read_excel(file)
    data = {'text': NLP.libraries.commandpreprocess_text(
        text), 'agenda': string, 'command': isqu}
    df = pd.DataFrame(read)
    new_row = pd.Series(data)
    df = df.append(new_row, ignore_index=True)
    df.to_excel(file, index=False)
