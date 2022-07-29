import NLP_package
from NLP_package import Tokenizers




class Model:
    
    EMBEDDING_VECTOR_LENGTH = 33
    
    def __init__(self):
        pass
    
    def createmodel(self):
        pass
    
    def train(self):
        pass
    

class BinaryLSTM(Model):

    def __init__(self, filemodelname, tokenizerfilename, dataselect,
                 recognizeddataselect):
        self.conn = NLP_package.psycopg2.connect(
            "dbname=postgres user=postgres password=postgres")
        self.filemodelname = filemodelname
        self.tokenizerfilename = tokenizerfilename
        self.dataselect = dataselect
        self.recognizeddataselect = recognizeddataselect

    def createmodel(self, tokenizer):
        optimzer = NLP_package.Adam(clipvalue=0.5)
        model = NLP_package.Sequential()
        model.add(NLP_package.Embedding(len(tokenizer.tokenizer.word_index) + 1,
                                        self.EMBEDDING_VECTOR_LENGTH,
                                        input_length=NLP_package.Tokenizers.CustomTokenizer.MAX_SEQUENCE_LENGTH,
                                        trainable=True, mask_zero=True))
        model.add(NLP_package.Dropout(0.5))
        model.add(NLP_package.LSTM(64, dropout=0.2, recurrent_dropout=0.2))
        model.add(NLP_package.Dense(512, activation="sigmoid"))
        model.add(NLP_package.Dropout(0.5))
        model.add(NLP_package.Dense(512, activation="sigmoid"))
        model.add(NLP_package.Dense(1, activation='sigmoid'))
        # compile the model
        model.compile(optimizer=optimzer, loss='binary_crossentropy',
                      metrics=['binary_accuracy'])

        return model

    def train(self, target, mode):

        recognizedtrain = NLP_package.pd.read_sql(self.recognizeddataselect, self.conn)
        recognizedtrain.text = recognizedtrain.text.astype(str)

        train = NLP_package.pd.read_sql(self.dataselect, self.conn)
        train.text = train.text.astype(str)

        df = NLP_package.pd.concat([train, recognizedtrain])
        train = df[~df[target].isna()]
        train[target] = train[target].astype(int)
        #train = train.drop_duplicates()

        print(train)
        X_train, X_val, y_train, y_val = NLP_package.train_test_split(
            train, train[target], test_size=0.3, random_state=32)

        if(mode == 'evaluate'):
            with open(self.tokenizerfilename, 'rb') as handle:
                tokenizer = NLP_package.p.load(handle)
        else:
            tokenizer = Tokenizers.CustomTokenizer(train_texts=X_train['text'])
            # fit o the train
        tokenizer.train_tokenize()
        tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
        tokenized_X_val = tokenizer.vectorize_input(X_val['text'])

        if(mode == 'evaluate'):
            model = NLP_package.load_model(self.filemodelname)
            
            es = NLP_package.EarlyStopping(patience=10, monitor='binary_accuracy',
                                           restore_best_weights=True)
            
            history = model.fit(tokenized_X_train, y_train,
                                validation_data=(tokenized_X_val, y_val),
                                batch_size=51,
                                epochs=200,
                                verbose=2,
                                callbacks=[es]
                                )
        else:
            model = self.createmodel(tokenizer)
            
            history = model.fit(tokenized_X_train, y_train,
                                validation_data=(tokenized_X_val, y_val),
                                batch_size=51,
                                epochs=250,
                                verbose=2,
                                )

        model.save(self.filemodelname)

        with open(self.tokenizerfilename, 'wb') as handle:
            NLP_package.p.dump(tokenizer, handle,
                               protocol=NLP_package.p.HIGHEST_PROTOCOL)



        s, (at, al) = NLP_package.plt.subplots(2, 1)
        at.plot(history.history['binary_accuracy'], c='b')
        at.plot(history.history['val_binary_accuracy'], c='r')
        at.set_title('model accuracy')
        at.set_ylabel('accuracy')
        at.set_xlabel('epoch')
        at.legend(['LSTM_train', 'LSTM_val'], loc='upper left')

        al.plot(history.history['loss'], c='m')
        al.plot(history.history['val_loss'], c='c')
        al.set_title('model loss')
        al.set_ylabel('loss')
        al.set_xlabel('epoch')
        al.legend(['train', 'val'], loc='upper left')

        fig = al.get_figure()
        fig.savefig('./models/binary/results_training/' + 'resultstraining_binary.png')


class MultyLSTM(Model):

    def __init__(self, filemodelname, tokenizerfilename, dataselect,
                 recognizeddataselect):
        self.conn = NLP_package.psycopg2.connect(
            "dbname=postgres user=postgres password=postgres")
        self.filemodelname = filemodelname
        self.tokenizerfilename = tokenizerfilename
        self.dataselect = dataselect
        self.recognizeddataselect = recognizeddataselect

    def createmodel(self, tokenizer, n_clases):
        model = NLP_package.Sequential()

        optimzer = NLP_package.Adam(learning_rate=0.005)
        model.add(NLP_package.Embedding(len(tokenizer.tokenizer.word_index) + 1,
                                        self.EMBEDDING_VECTOR_LENGTH,
                                        input_length=NLP_package.Tokenizers.CustomTokenizer.MAX_SEQUENCE_LENGTH,
                                        trainable=True))
        model.add(NLP_package.Bidirectional(NLP_package.LSTM(256, dropout=0.2,recurrent_dropout=0.2, return_sequences=True)))
        model.add(NLP_package.Bidirectional(NLP_package.LSTM(128, dropout=0.2, recurrent_dropout=0.2, return_sequences=True)))
        model.add(NLP_package.Bidirectional(NLP_package.LSTM(128, dropout=0.2, recurrent_dropout=0.2)))
        model.add(NLP_package.Dense(n_clases, activation='softmax'))
        # compile the model
        model.compile(optimizer=optimzer, loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def train(self, target, n_clases, mode):

        train = NLP_package.pd.read_sql(self.dataselect, self.conn)
        train.text = train.text.astype(str)
        recognizedtrain = NLP_package.pd.read_sql(
            self.recognizeddataselect, self.conn)
        recognizedtrain.text = recognizedtrain.text.astype(str)
        df = NLP_package.pd.concat([train, recognizedtrain])
        train = df[~df[target].isna()]
        train[target] = train[target].astype(int)
        train = train.drop_duplicates()

        X_train, X_val, y_train, y_val = NLP_package.train_test_split(
            train, train[target], test_size=0.2, random_state=64)
        print('Shape of train', X_train.shape)
        print("Shape of Validation ", X_val.shape)

        if(mode == 'evaluate'):
            with open(self.tokenizerfilename,
                      'rb') as handle:
                tokenizer = NLP_package.p.load(handle)
        else:
            tokenizer = Tokenizers.CustomTokenizer(train_texts=X_train['text'])
            # fit o the train
        tokenizer.train_tokenize()
        tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
        tokenized_X_val = tokenizer.vectorize_input(X_val['text'])


        y_trainmatrix = NLP_package.tensorflow.keras.utils.to_categorical(
            y_train, n_clases)
        y_valmatrix = NLP_package.tensorflow.keras.utils.to_categorical(
            y_val, n_clases)
        if(mode == 'evaluate'):
            
            es = NLP_package.EarlyStopping(patience=2, monitor='val_loss',
                                           restore_best_weights=True)

            model = NLP_package.load_model(self.filemodelname)
            
            history = model.fit(tokenized_X_train, y_trainmatrix,
                                batch_size=51, epochs=50,
                                validation_data=(tokenized_X_val, y_valmatrix),
                                verbose=2,
                                callbacks=[es])
        else:
            model = self.createmodel(tokenizer, n_clases)

            history = model.fit(tokenized_X_train, y_trainmatrix,
                                batch_size=51, epochs=13,
                                validation_data=(tokenized_X_val, y_valmatrix),
                                verbose=2)

        model.save(self.filemodelname)

        with open(self.tokenizerfilename, 'wb') as handle:
            NLP_package.p.dump(tokenizer, handle,
                               protocol=NLP_package.p.HIGHEST_PROTOCOL)


class NonNeuro(Model):
    def __init__(self,filemodelname, tokenizerfilename, dataselect,
                 recognizeddataselect):
        self.conn = NLP_package.psycopg2.connect(
            "dbname=postgres user=postgres password=postgres")
        self.filemodelname = filemodelname
        self.tokenizerfilename = tokenizerfilename
        self.dataselect = dataselect
        self.recognizeddataselect = recognizeddataselect


    def createmodel(self):
        nb_model = NLP_package.MultinomialNB()
        return nb_model

    def train(self, target, mode):
        train = NLP_package.pd.read_sql(self.dataselect, self.conn)
        recognizedtrain = NLP_package.pd.read_sql(self.recognizeddataselect, self.conn)
        df = NLP_package.pd.concat([train, recognizedtrain])

        train = df[~df[target].isna()]
        train[target] = train[target].astype(int)
        train = train.drop_duplicates()
        ds = NLP_package.DataShowers.DataShower()
        ds.showdata(train, target)

        nb_x, nb_x_test, nb_y, nb_y_test = NLP_package.train_test_split(train['text'], train[target], test_size=0.3,
                                                            random_state=32)
        vec = NLP_package.CountVectorizer()
        nb_x = vec.fit_transform(nb_x).toarray()
        nb_x_test = vec.transform(nb_x_test).toarray()

        nb_model = self.createmodel()

        nb_model.fit(nb_x, nb_y)

        with open(self.tokenizerfilename, 'wb') as handle:
            NLP_package.p.dump(vec, handle,
                               protocol=NLP_package.p.HIGHEST_PROTOCOL)

        with open(self.filemodelname, 'wb') as handle:
            NLP_package.p.dump(nb_model, handle,
                               protocol=NLP_package.p.HIGHEST_PROTOCOL)