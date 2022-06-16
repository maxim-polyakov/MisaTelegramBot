import pandas as pd
import random
import NLP
from NLP import mapa
from sqlalchemy import create_engine

class Answer:

    def __init__(self):
        pass

    def answer(self):
        pass


class RandomAnswer(Answer):
    
    conn = NLP.psycopg2.connect("dbname=postgres user=postgres password=postgres")

    inpt = pd.read_sql('SELECT * FROM hiset', conn)

    data = NLP.pd.concat([inpt])
    df = []


    def __init__(self):
        pass

    def answer(self):
        
        
        
        outmapa = []
        for i in range(0, len(self.data['text'])-1):
            if(self.data['hi'][i] == 1):
                self.df.append(self.data['text'][i])
        print(self.df)
        outmapa = {0: [self.df[random.randint(0, len(self.df))]]}
                
        return (outmapa[0])
