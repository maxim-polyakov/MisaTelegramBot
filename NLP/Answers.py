import pandas as pd
import random
from NLP import mapa


class Answer:

    def __init__(self):
        pass

    def answer(self):
        pass


class RandomAnswer(Answer):

    data = pd.read_excel('./datasets/dataset.xlsx')
    df = []

    def __init__(self):
        pass

    def answer(self):
        outmapa = []
        for i in range(0, len(self.data['text'])-1):
            if(self.data['hi'][i] == 1):
                self.df.append(self.data['text'][i])
                outmapa = {0: [self.df[random.randint(0, len(self.df))]]}
                return (outmapa[0])
