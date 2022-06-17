import NLP
from NLP import Tokenizers
from NLP import DataShowers
from NLP import TextPreprocessers




class Model:
    
    EMBEDDING_VECTOR_LENGTH = 33
    
    def __init__(self):
        pass
    
    def createmodel(self):
        pass
    
    def train(self):
        pass
    

class Binary(Model):

    def __init__(self, filemodelname, tokenizerfilename, dataselect,
                 recognizeddataselect):
        self.conn = NLP.psycopg2.connect(
            "dbname=postgres user=postgres password=postgres")
        self.filemodelname = filemodelname
        self.tokenizerfilename = tokenizerfilename
        self.dataselect = dataselect
        self.recognizeddataselect = recognizeddataselect

    def createmodel(self, tokenizer):
        optimzer = NLP.Adam(clipvalue=0.5)
        model = NLP.Sequential()
        model.add(NLP.Embedding(len(tokenizer.tokenizer.word_index)+1,
                                self.EMBEDDING_VECTOR_LENGTH,
                  input_length=Tokenizers.CustomTokenizer.MAX_SEQUENCE_LENGTH,
                  trainable=True, mask_zero=True))
        model.add(NLP.Dropout(0.1))
        model.add(NLP.LSTM(64))
        model.add(NLP.Dense(64, activation="sigmoid"))
        model.add(NLP.Dense(32, activation="sigmoid"))
        model.add(NLP.Dense(16, activation="sigmoid"))
        model.add(NLP.Dense(1, activation='sigmoid'))
        # compile the model
        model.compile(optimizer=optimzer, loss='binary_crossentropy',
                      metrics=['binary_accuracy'])

        return model

    def train(self, target, mode):

        recognizedtrain = NLP.pd.read_sql(self.recognizeddataselect, self.conn)
        recognizedtrain.text = recognizedtrain.text.astype(str)

        train = NLP.pd.read_sql(self.dataselect, self.conn)
        train.text = train.text.astype(str)

        df = NLP.pd.concat([train, recognizedtrain])
        train = df[~df[target].isna()]
        train[target] = train[target].astype(int)
        train = train.drop_duplicates()
        ds = DataShowers.DataShower()
        ds.showdata(train, target)

        X_train, X_val, y_train, y_val = NLP.train_test_split(
            train, train[target], test_size=0.3, random_state=32)

        if(mode == 'evaluate'):
            with open(self.tokenizerfilename, 'rb') as handle:
                tokenizer = NLP.p.load(handle)
        else:
            tokenizer = Tokenizers.CustomTokenizer(train_texts=X_train['text'])
            # fit o the train
        tokenizer.train_tokenize()
        tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
        tokenized_X_val = tokenizer.vectorize_input(X_val['text'])

        if(mode == 'evaluate'):
            model = NLP.load_model(self.filemodelname)
            
            es = NLP.EarlyStopping(patience=10, monitor='binary_accuracy', restore_best_weights=True)
            
            history = model.fit(tokenized_X_train, y_train,
                                validation_data=(tokenized_X_val, y_val),
                                batch_size=512,
                                epochs=2000,
                                verbose=2,
                                callbacks=[es]
                                )
        else:
            model = self.createmodel(tokenizer)
            
            history = model.fit(tokenized_X_train, y_train,
                                validation_data=(tokenized_X_val, y_val),
                                batch_size=512,
                                epochs=2000,
                                verbose=2,
                                )

        model.save(self.filemodelname)

        with open(self.tokenizerfilename, 'wb') as handle:
            NLP.p.dump(tokenizer, handle,
                       protocol=NLP.p.HIGHEST_PROTOCOL)


class Multy(Model):

    def __init__(self, filemodelname, tokenizerfilename, dataselect,
                 recognizeddataselect):
        self.conn = NLP.psycopg2.connect(
            "dbname=postgres user=postgres password=postgres")
        self.filemodelname = filemodelname
        self.tokenizerfilename = tokenizerfilename
        self.dataselect = dataselect
        self.recognizeddataselect = recognizeddataselect

    def createmodel(self, tokenizer, n_clases):
        model = NLP.Sequential()
        optimzer = NLP.Adam(clipvalue=0.5)
        model.add(NLP.Embedding(len(tokenizer.tokenizer.word_index)+1,
                                self.EMBEDDING_VECTOR_LENGTH,
                                input_length=Tokenizers.CustomTokenizer.MAX_SEQUENCE_LENGTH, trainable=True))
        model.add(NLP.LSTM(100, dropout=0.2, recurrent_dropout=0.5))
        model.add(NLP.Dense(64, activation="sigmoid"))
        model.add(NLP.Dense(32, activation="sigmoid"))
        model.add(NLP.Dense(16, activation="sigmoid"))
        model.add(NLP.Dense(n_clases, activation='softmax'))
        # compile the model
        model.compile(optimizer=optimzer, loss='categorical_crossentropy', metrics=[
            'categorical_accuracy'])
        return model

    def train(self, target, n_clases, mode):

        train = NLP.pd.read_sql(self.dataselect, self.conn)
        train.text = train.text.astype(str)
        recognizedtrain = NLP.pd.read_sql(
            self.recognizeddataselect, self.conn)
        recognizedtrain.text = recognizedtrain.text.astype(str)
        df = NLP.pd.concat([train, recognizedtrain])
        train = df[~df[target].isna()]
        train[target] = train[target].astype(int)
        train = train.drop_duplicates()

        ds = DataShowers.DataShower()
        ds.showdata(train, target)
        X_train, X_val, y_train, y_val = NLP.train_test_split(
            train, train[target], test_size=0.2, random_state=64)
        print('Shape of train', X_train.shape)
        print("Shape of Validation ", X_val.shape)

        if(mode == 'evaluate'):
            with open(self.tokenizerfilename,
                      'rb') as handle:
                tokenizer = NLP.p.load(handle)
        else:
            tokenizer = Tokenizers.CustomTokenizer(train_texts=X_train['text'])
            # fit o the train
        tokenizer.train_tokenize()
        tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
        tokenized_X_val = tokenizer.vectorize_input(X_val['text'])


        y_trainmatrix = NLP.tensorflow.keras.utils.to_categorical(
            y_train, n_clases)
        y_valmatrix = NLP.tensorflow.keras.utils.to_categorical(
            y_val, n_clases)
        if(mode == 'evaluate'):
            
            es = NLP.EarlyStopping(patience=10, monitor='val_accuracy', restore_best_weights=True)
            
            model = NLP.load_model(self.filemodelname)
            
            history = model.fit(tokenized_X_train, y_trainmatrix,
                                batch_size=64, epochs=4000,
                                validation_data=(tokenized_X_val, y_valmatrix),
                                callbacks=[es],
                                verbose=2)
        else:
            model = self.createmodel(tokenizer, n_clases)
            
            history = model.fit(tokenized_X_train, y_trainmatrix,
                                batch_size=64, epochs=4000,
                                validation_data=(tokenized_X_val, y_valmatrix),
                                verbose=2)



        #loss, acc = model.evaluate(tokenized_X_val, y_valmatrix, verbose=2)

        model.save(self.filemodelname)

        with open(self.tokenizerfilename, 'wb') as handle:
            NLP.p.dump(tokenizer, handle,
                       protocol=NLP.p.HIGHEST_PROTOCOL)
