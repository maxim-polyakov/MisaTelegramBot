import Command_package

class DataShower:

    def __init__(self, bot, message, dataselect,
                 recognizeddataselect):

        self.conn = Command_package.psycopg2.connect(
        "dbname=postgres user=postgres password=postgres")

        self.bot = bot
        self.message = message
        self.dataselect = dataselect
        self.recognizeddataselect = recognizeddataselect


    def showdata(self, target):

        recognizedtrain = Command_package.pd.read_sql(self.recognizeddataselect, self.conn)
        recognizedtrain.text = recognizedtrain.text.astype(str)

        train = Command_package.pd.read_sql(self.dataselect, self.conn)
        train.text = train.text.astype(str)

        df = Command_package.pd.concat([train, recognizedtrain])
        train = df[~df[target].isna()]
        train[target] = train[target].astype(int)
        train = train.drop_duplicates()

        key_metrics = {'samples': len(train),
                       'samples_per_class': train[target].value_counts().median(),
                       'median_of_samples_lengths': Command_package.np.median(train['text'].str.split().map(lambda x: len(x))),
                       }
        key_metrics = Command_package.pd.DataFrame.from_dict(
            key_metrics, orient='index').reset_index()
        key_metrics.columns = ['metric', 'value']
        green = '#52BE80'
        red = '#EC7063'

        outt = Command_package.sns.countplot(train[target])
        fig = outt.get_figure()
        fig.savefig('./Command_package/outputs/outcountplot.png')




        self.bot.send_photo(self.message.chat.id, photo=open('./Command_package/outputs/outcountplot.png', 'rb'),
                        parse_mode='html')

        self.bot.send_message(self.message.chat.id, "Дисперсия " +str(Command_package.np.var(train[target])) +
                              " Медиана " +str(Command_package.np.median(train[target])) +
                              " Мат ожидание " +str(Command_package.np.mean(train[target])) +
                              " Стандартное отклонение " +str(Command_package.np.std(train[target])), parse_mode='html')


