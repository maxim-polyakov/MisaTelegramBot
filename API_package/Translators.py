import API_package

class Translator:
    def __init__(self):
        pass
    def translate(self):
        pass

class GoogleTranslator(Translator):

    __conn = API_package.psycopg2.connect(
        "dbname=postgres user=postgres password=postgres")

    __engine = API_package.create_engine(
        'postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')

    __translator = API_package.Translator()

    def __init__(self, lang):
        self.lang = lang

    def __translate(self, text):
        tranlated = self.__translator.translate(text, dest=self.lang)
        return tranlated.text

    def translate(self, boto, message, inptmes):
        tranlated = self.__translate(inptmes)

        boto.send_message(message.chat.id, tranlated, parse_mode='html')



    def translatedt(self, dataselect, insertdtname):

        train = API_package.pd.read_sql(dataselect, self.__conn)
        train.text = train.text.astype(str)

        df = API_package.pd.concat([train])

        df['text'] = df['text'].apply(self.__translate)
        df.to_sql(insertdtname, con = self.__engine, schema = 'public',
                  index=False, if_exists = 'append')


