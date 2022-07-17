import Bot_package


from sqlalchemy import create_engine


class Subfuncion:
    def __init__(self):
        pass

class Adder(Subfuncion):
    def __init__(self):
        pass

    def add(text, tablename, string, agenda, classification, classtype):
        pr = Bot_package.TextPreprocessers.CommonPreprocessing()
        conn = Bot_package.psycopg2.connect("dbname=postgres user=postgres password=postgres")
        engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
        data = {'text': pr.preprocess_text(
            text), agenda: string, classification: classtype}
        df = Bot_package.pd.DataFrame()
        new_row = Bot_package.pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql(tablename, con=engine, schema='public', index=False, if_exists='append')

    def quadd(text, tablename, string, isqu):
        pr = Bot_package.TextPreprocessers.QuestionPreprocessing()
        conn = Bot_package.psycopg2.connect("dbname=postgres user=postgres password=postgres")
        engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
        data = {'text': pr.preprocess_text(
            text), 'agenda': string, 'question': isqu}
        df = Bot_package.pd.DataFrame()
        new_row = Bot_package.pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql(tablename, con=engine, schema='public', index=False, if_exists='append')

    def commandadd(text, tablename, string, isqu):
        pr = Bot_package.CommandPreprocessing()
        conn = Bot_package.TextPreprocessers.psycopg2.connect("dbname=postgres user=postgres password=postgres")
        engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')
        data = {'text': pr.preprocess_text(
            text), 'agenda': string, 'command': isqu}
        df = Bot_package.pd.DataFrame()
        new_row = Bot_package.pd.Series(data)
        df = df.append(new_row, ignore_index=True)
        df.to_sql(tablename, con=engine, schema='public', index=False, if_exists='append')
