import pandas as pd
from NLP_package import TextPreprocessers
import NLP_package
from sqlalchemy import create_engine


class Subfuncion:
    def __init__(self):
        pass

class Adder:
    def __init__(self):
        pass

    def add(text, tablename, string, agenda, classification, classtype):
        pr = TextPreprocessers.CommonPreprocessing()
        conn = NLP_package.psycopg2.connect("dbname=postgres user=postgres password=postgres")
        engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
        data = {'text': pr.preprocess_text(
            text), agenda: string, classification: classtype}
        df = pd.DataFrame()
        new_row = pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql(tablename, con=engine, schema='public', index=False, if_exists='append')

    def quadd(text, tablename, string, isqu):
        pr = TextPreprocessers.QuestionPreprocessing()
        conn = NLP_package.psycopg2.connect("dbname=postgres user=postgres password=postgres")
        engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
        data = {'text': pr.preprocess_text(
            text), 'agenda': string, 'question': isqu}
        df = pd.DataFrame()
        new_row = pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql(tablename, con=engine, schema='public', index=False, if_exists='append')

    def commandadd(text, tablename, string, isqu):
        pr = NLP_package.CommandPreprocessing()
        conn = TextPreprocessers.psycopg2.connect("dbname=postgres user=postgres password=postgres")
        engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
        data = {'text': pr.preprocess_text(
            text), 'agenda': string, 'command': isqu}
        df = pd.DataFrame()
        new_row = pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql(tablename, con=engine, schema='public', index=False, if_exists='append')
