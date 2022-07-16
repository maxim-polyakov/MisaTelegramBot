import API_package

class DataShower:

    def __init__(self, bot, message, dataselect,
                 recognizeddataselect):

        self.conn = API_package.psycopg2.connect(
        "dbname=postgres user=postgres password=postgres")

        self.bot = bot
        self.message = message
        self.dataselect = dataselect
        self.recognizeddataselect = recognizeddataselect


    def showdata(self, target):

        recognizedtrain = API_package.pd.read_sql(self.recognizeddataselect, self.conn)
        recognizedtrain.text = recognizedtrain.text.astype(str)

        train = API_package.pd.read_sql(self.dataselect, self.conn)
        train.text = train.text.astype(str)

        df = API_package.pd.concat([train])
        train = df[~df[target].isna()]
        train[target] = train[target].astype(int)
        train = train.drop_duplicates()

        key_metrics = {'samples': len(train),
                       'samples_per_class': train[target].value_counts().median(),
                       'median_of_samples_lengths': API_package.np.median(train['text'].str.split().map(lambda x: len(x))),
                       }
        key_metrics = API_package.pd.DataFrame.from_dict(
            key_metrics, orient='index').reset_index()
        key_metrics.columns = ['metric', 'value']
        green = '#52BE80'
        red = '#EC7063'

        outt = API_package.sns.countplot(train[target])
        fig = outt.get_figure()
        fig.savefig('./API_package/outputs/outcountplot.png')

        API_package.plt.figure(figsize=(16, 7))
        API_package.plt.hist(sample, bins=30, density=True,
                 alpha=0.6, label='Гистограмма выборки')
        API_package.plt.plot(grid, sps.norm.pdf(grid), color='red',
                 lw=5, label='Плотность случайной величины')
        API_package.plt.title(r'Случайная величина $\xi \sim \mathcal{N}$(0, 1)', fontsize=20)
        API_package.plt.legend(fontsize=14, loc=1)
        API_package.plt.grid(ls=':')
        API_package.plt.show()


        self.bot.send_photo(self.message.chat.id, photo=open('./API_package/outputs/output.png', 'rb'),
                        parse_mode='html')

        self.bot.send_message(self.message.chat.id, "Дисперсия " +str(API_package.np.var(train[target])),
                          parse_mode='html')

        self.bot.send_message(self.message.chat.id, "Медиана  " +str(API_package.np.median(train[target])),
                          parse_mode='html')

        self.bot.send_message(self.message.chat.id, "Мат ожидание  " +str(API_package.np.mean(train[target])),
                          parse_mode='html')

        self.bot.send_message(self.message.chat.id, "Стандартное отклонение  " +str(API_package.np.std(train[target])),
                          parse_mode='html')


