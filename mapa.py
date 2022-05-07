import pandas as pd
import random

data = pd.read_excel('./datasets/dataset.xlsx')
df = []

def randanswhi():
    outmapa = []
    for i in range(0,len(data['text'])-1):
        if(data['hi'][i] == 1):
            df.append(data['text'][i])
    outmapa = {0:[df[random.randint(0,len(df))]]}
    return (outmapa[0])

def randansww():
    outmapa = []
    for i in range(0,len(data['text'])-1):
        if(data['weather'][i] == 1):
            df.append(data['text'][i])
    outmapa = {0:[df[random.randint(0,len(df))]]}
    return (outmapa[0])

himapa = {0:"Не приветствие", 1:"Приветствие"}
qumapa = {0:"Не вопрос", 1:"Вопрос"}
thmapa = {0:"Не благодарность", 1:"Благодарность"}


multymapa = {0:"Нет темы", 1:"Погода", 2:"Дело"}

