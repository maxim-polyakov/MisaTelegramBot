import libraries
import mapa
from tensorflow.keras.models import load_model


def showdata(train, target):
    key_metrics = {'samples': len(train),
                   'samples_per_class': train[target].value_counts().median(),
                   'median_of_samples_lengths': libraries.np.median(train['text'].str.split().map(lambda x: len(x))),
                   }
    key_metrics = libraries.pd.DataFrame.from_dict(
        key_metrics, orient='index').reset_index()
    key_metrics.columns = ['metric', 'value']
    green = '#52BE80'
    red = '#EC7063'
    libraries.sns.countplot(train[target], palette=[green, red])


def DataCleaner(filename, string):
    train = libraries.pd.read_excel(filename)
    train.text = train.text.astype(str)
    df = libraries.pd.concat([train])
    df['text'] = df['text'].apply(libraries.preprocess_text)
    train = df[~df[string].isna()]
    train[string] = train[string].astype(int)
    train.to_excel(filename, index=False)


def QuestionsetCleaner(filename):
    train = libraries.pd.read_excel(filename)
    train.text = train.text.astype(str)
    df = libraries.pd.concat([train])
    df['text'] = df['text'].apply(libraries.specialpreprocess_text)
    train = df[~df['question'].isna()]
    train['question'] = train['question'].astype(int)
    train.to_excel(filename, index=False)


def CommandsetCleaner(filename):
    train = libraries.pd.read_excel(filename)
    train.text = train.text.astype(str)
    df = libraries.pd.concat([train])
    df['text'] = df['text'].apply(libraries.commandpreprocess_text)
    train = df[~df['command'].isna()]
    train['command'] = train['command'].astype(int)
    train.to_excel(filename, index=False)


class Binary:

    def __init__(self, filemodelname, tokenizerfilename, datafilename,
                 recognizeddatafilename):
        self.filemodelname = filemodelname
        self.tokenizerfilename = tokenizerfilename
        self.datafilename = datafilename
        self.recognizeddatafilename = recognizeddatafilename

    def CreateModel_bin(tokenizer):
        optimzer = libraries.Adam(clipvalue=0.5)
        model = libraries.Sequential()
        model.add(libraries.Embedding(len(tokenizer.tokenizer.word_index)+1,
                                      libraries.EMBEDDING_VECTOR_LENGTH,
                  input_length=libraries.MAX_SEQUENCE_LENGTH,
                  trainable=True, mask_zero=True))
        model.add(libraries.Dropout(0.1))
        model.add(libraries.LSTM(64))
        model.add(libraries.Dense(64, activation="sigmoid"))
        model.add(libraries.Dense(32, activation="sigmoid"))
        model.add(libraries.Dense(16, activation="sigmoid"))
        model.add(libraries.Dense(1, activation='sigmoid'))
        # compile the model
        model.compile(optimizer=optimzer, loss='binary_crossentropy',
                      metrics=['binary_accuracy'])

        return model

    def binary(self, target, mode):
        self.recognizedtrain = libraries.pd.read_excel(
            self.recognizeddatafilename)
        self.recognizedtrain.text = self.recognizedtrain.text.astype(str)

        train = libraries.pd.read_excel(self.datafilename)
        train.text = train.text.astype(str)

        df = libraries.pd.concat([train, self.recognizedtrain])
        train = df[~df[target].isna()]
        train[target] = train[target].astype(int)
        train = train.drop_duplicates()

        showdata(train, target)
        X_train, X_val, y_train, y_val = libraries.train_test_split(
            train, train[target], test_size=0.3, random_state=32)

        if(mode == 'evaluate'):
            with open(self.tokenizerfilename, 'rb') as handle:
                tokenizer = libraries.p.load(handle)
        else:
            tokenizer = libraries.CustomTokenizer(train_texts=X_train['text'])
            # fit o the train
            tokenizer.train_tokenize()
            tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
            tokenized_X_val = tokenizer.vectorize_input(X_val['text'])

        if(mode == 'evaluate'):
            model = load_model(self.filemodelname)
        else:
            model = self.CreateModel_bin(tokenizer)

        history = model.fit(tokenized_X_train, y_train,
                            validation_data=(tokenized_X_val, y_val),
                            batch_size=512,
                            epochs=2000,
                            verbose=2,
                            )
        model.save(self.filemodelname)

        with open(self.tokenizerfilename, 'wb') as handle:
            libraries.p.dump(tokenizer, handle,
                             protocol=libraries.p.HIGHEST_PROTOCOL)


class Multy:

    def __init__(self):
        self.filemodelname = './models/multy/multyclassmodel.h5'
        self.tokenizerfilename = './tokenizers/multy/multyclasstokenizer.pickle'
        self.datafilename = './datasets/multyclasesset.xlsx'
        self.recognizeddatafilename = './recognized_sets/recognized_multyclass.xlsx'

    def CreateModel_mul(self, tokenizer, n_clases):
        model = libraries.Sequential()
        optimzer = libraries.Adam(clipvalue=0.5)
        model.add(libraries.Embedding(len(tokenizer.tokenizer.word_index)+1,
                                      libraries.EMBEDDING_VECTOR_LENGTH,
                                      input_length=libraries.MAX_SEQUENCE_LENGTH, trainable=True))
        model.add(libraries.LSTM(100, dropout=0.2, recurrent_dropout=0.5))
        model.add(libraries.Dense(64, activation="sigmoid"))
        model.add(libraries.Dense(32, activation="sigmoid"))
        model.add(libraries.Dense(16, activation="sigmoid"))
        model.add(libraries.Dense(n_clases, activation='softmax'))
        # compile the model
        model.compile(optimizer=optimzer, loss='categorical_crossentropy', metrics=[
            'categorical_accuracy'])
        return model

    def multyclasstrain(self, mode):

        train = libraries.pd.read_excel(self.datafilename)
        train.text = train.text.astype(str)
        recognizedtrain = libraries.pd.read_excel(
            self.recognizeddatafilename)
        recognizedtrain.text = recognizedtrain.text.astype(str)
        df = libraries.pd.concat([train, recognizedtrain])
        train = df[~df['questionclass'].isna()]
        train['questionclass'] = train['questionclass'].astype(int)
        train = train.drop_duplicates()
        target = 'questionclass'
        showdata(train, target)
        X_train, X_val, y_train, y_val = libraries.train_test_split(
            train, train['questionclass'], test_size=0.2, random_state=64)
        print('Shape of train', X_train.shape)
        print("Shape of Validation ", X_val.shape)

        if(mode == 'evaluate'):
            with open(self.tokenizerfilename,
                      'rb') as handle:
                tokenizer = libraries.p.load(handle)
        else:
            tokenizer = libraries.CustomTokenizer(train_texts=X_train['text'])
            # fit o the train
        tokenizer.train_tokenize()
        tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
        tokenized_X_val = tokenizer.vectorize_input(X_val['text'])

        n_clases = 3
        y_trainmatrix = libraries.tensorflow.keras.utils.to_categorical(
            y_train, n_clases)
        y_valmatrix = libraries.tensorflow.keras.utils.to_categorical(
            y_val, n_clases)
        if(mode == 'evaluate'):
            model = load_model(self.filemodelname)
        else:
            model = self.CreateModel_mul(tokenizer, n_clases)

        history = model.fit(tokenized_X_train, y_trainmatrix,
                            batch_size=64, epochs=2000,
                            validation_data=(tokenized_X_val, y_valmatrix),
                            verbose=2)

        #loss, acc = model.evaluate(tokenized_X_val, y_valmatrix, verbose=2)

        model.save(self.filemodelname)

        with open(self.tokenizerfilename, 'wb') as handle:
            libraries.p.dump(tokenizer, handle,
                             protocol=libraries.p.HIGHEST_PROTOCOL)
