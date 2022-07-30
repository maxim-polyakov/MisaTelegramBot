import NLP_package



class DataShowerSns:

    def showdata(self, train, target):
        key_metrics = {'samples': len(train),
                       'samples_per_class': train[target].value_counts().median(),
                       'median_of_samples_lengths': NLP_package.np.median(train['text'].str.split().map(lambda x: len(x))),
                       }
        key_metrics = NLP_package.pd.DataFrame.from_dict(
            key_metrics, orient='index').reset_index()
        key_metrics.columns = ['metric', 'value']
        green = '#52BE80'
        red = '#EC7063'
        NLP_package.sns.countplot(train[target], palette=[green, red])


