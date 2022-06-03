import pandas as pd
import NLP
from sqlalchemy import create_engine

def add(text, tablename, string, agenda, classification, classtype):
    conn = NLP.psycopg2.connect("dbname=postgres user=postgres password=postgres")
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
    data = {'text': NLP.NLP.preprocess_text(
        text), agenda: string, classification: classtype}
    df = pd.DataFrame()
    new_row = pd.Series(data)
    df = df.append(new_row, ignore_index=True)
    df.to_sql(tablename, con = engine, schema = 'public', index=False, if_exists='append')


def quadd(text, tablename, string, isqu):
    conn = NLP.psycopg2.connect("dbname=postgres user=postgres password=postgres")
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
    data = {'text': NLP.NLP.specialpreprocess_text(
        text), 'agenda': string, 'question': isqu}
    df = pd.DataFrame()
    new_row = pd.Series(data)
    df = df.append(new_row, ignore_index=True)
    df.to_sql(tablename, con = engine, schema = 'public', index=False, if_exists='append')
    
def commandadd(text, tablename, string, isqu):
    conn = NLP.psycopg2.connect("dbname=postgres user=postgres password=postgres")
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
    data = {'text': NLP.NLP.commandpreprocess_text(
        text), 'agenda': string, 'command': isqu}
    df = pd.DataFrame()
    new_row = pd.Series(data)
    df = df.append(new_row, ignore_index=True)
    df.to_sql(tablename, con = engine, schema = 'public', index=False, if_exists='append')
