import NLP

mystem = NLP.Mystem()

TOP_K = 20000
EMBEDDING_VECTOR_LENGTH = 33
MAX_SEQUENCE_LENGTH = 33
russian_stopwords = NLP.stopwords.words("russian")
english_stopwords = NLP.stopwords.words("english")

def showdata(train, target):
    key_metrics = {'samples': len(train),
                   'samples_per_class': train[target].value_counts().median(),
                   'median_of_samples_lengths': NLP.np.median(train['text'].str.split().map(lambda x: len(x))),
                   }
    key_metrics = NLP.pd.DataFrame.from_dict(
        key_metrics, orient='index').reset_index()
    key_metrics.columns = ['metric', 'value']
    green = '#52BE80'
    red = '#EC7063'
    NLP.sns.countplot(train[target], palette=[green, red])

def remove_punctuation(text):
    
    translator = str.maketrans('', '', NLP.string.punctuation)
    return text.translate(translator)
def preprocess_text(text):
    try:
        tokens = str(text)
        tokens = mystem.lemmatize(text.lower())
        tokens = [token for token in tokens if token not in russian_stopwords
                  and token != " "
                  and token.strip() not in NLP.punctuation]
        tokens = [token for token in tokens if token not in english_stopwords]

        text = " ".join(tokens).rstrip('\n')
        pattern3 = r"[\d]"
        pattern2 = "[.]"
        text = NLP.re.sub(pattern3, "", text)
        text = NLP.re.sub(pattern2, "", text)
        text = remove_punctuation(text)
        return text
    except:
        return "except"

def specialpreprocess_text(text):
    try:
        tokens = str(text)
        tokens = mystem.lemmatize(text.lower())
        pattern2 = "[?]"
        pattern3 = r"[\d]"
        text = NLP.re.sub(pattern2, "", text)
        text = NLP.re.sub(pattern3, "", text)
        text = remove_punctuation(text)
        text = "".join(tokens).rstrip('\n')
        return text
    except:
        return "except"

def commandpreprocess_text(text):
    try:
        tokens = text.lower().rstrip('\n')
        text = "".join(tokens)

        return text
    except:
        return "except"



def DataCleaner(filename, string):
    train = NLP.pd.read_excel(filename)
    train.text = train.text.astype(str)
    df = NLP.pd.concat([train])
    df['text'] = df['text'].apply(preprocess_text)
    train = df[~df[string].isna()]
    train[string] = train[string].astype(int)
    train.to_excel(filename, index=False)

def QuestionsetCleaner(filename):
    train = NLP.pd.read_excel(filename)
    train.text = train.text.astype(str)
    df = NLP.pd.concat([train])
    df['text'] = df['text'].apply(specialpreprocess_text)
    train = df[~df['question'].isna()]
    train['question'] = train['question'].astype(int)
    train.to_excel(filename, index=False)

def CommandsetCleaner(filename):
    train = NLP.pd.read_excel(filename)
    train.text = train.text.astype(str)
    df = NLP.pd.concat([train])
    df['text'] = df['text'].apply(commandpreprocess_text)
    train = df[~df['command'].isna()]
    train['command'] = train['command'].astype(int)
    train.to_excel(filename, index=False)


class CustomTokenizer:
    def __init__(self, train_texts):
        self.train_texts = train_texts
        self.tokenizer = NLP.Tokenizer(num_words=TOP_K)

    def train_tokenize(self):
        # Get max sequence length.
        max_length = len(max(self.train_texts, key=len))
        self.max_length = min(max_length, MAX_SEQUENCE_LENGTH)

        # Create vocabulary with training texts.
        self.tokenizer.fit_on_texts(self.train_texts)

    def vectorize_input(self, tweets):
        # Vectorize training and validation texts.

        tweets = self.tokenizer.texts_to_sequences(tweets)
        # Fix sequence length to max value. Sequences shorter than the length are
        # padded in the beginning and sequences longer are truncated
        # at the beginning.
        tweets = NLP.pad_sequences(
            tweets, maxlen=self.max_length, truncating='post', padding='post')
        return tweets

class Binary:

    def __init__(self, filemodelname, tokenizerfilename, dataselect,
                 recognizeddataselect):
        self.conn = NLP.psycopg2.connect("dbname=postgres user=postgres password=postgres")
        self.filemodelname = filemodelname
        self.tokenizerfilename = tokenizerfilename
        self.dataselect = dataselect
        self.recognizeddataselect = recognizeddataselect

    def CreateModel_bin(self, tokenizer):
        optimzer = NLP.Adam(clipvalue=0.5)
        model = NLP.Sequential()
        model.add(NLP.Embedding(len(tokenizer.tokenizer.word_index)+1,
                                      EMBEDDING_VECTOR_LENGTH,
                  input_length=MAX_SEQUENCE_LENGTH,
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

    def binary(self, target, mode):
        
       
        recognizedtrain = NLP.pd.read_sql(self.recognizeddataselect, self.conn)
        recognizedtrain.text = recognizedtrain.text.astype(str)
        
        
        
        train = NLP.pd.read_sql(self.dataselect, self.conn)
        train.text = train.text.astype(str)
        
        df = NLP.pd.concat([train,recognizedtrain])
        train = df[~df[target].isna()]
        train[target] = train[target].astype(int)
        train = train.drop_duplicates()

        showdata(train, target)
        X_train, X_val, y_train, y_val = NLP.train_test_split(
            train, train[target], test_size=0.3, random_state=32)

        if(mode == 'evaluate'):
            with open(self.tokenizerfilename, 'rb') as handle:
                tokenizer = NLP.p.load(handle)
        else:
            tokenizer = CustomTokenizer(train_texts=X_train['text'])
            # fit o the train
        tokenizer.train_tokenize()
        tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
        tokenized_X_val = tokenizer.vectorize_input(X_val['text'])

        if(mode == 'evaluate'):
            model = NLP.load_model(self.filemodelname)
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
            NLP.p.dump(tokenizer, handle,
                             protocol=NLP.p.HIGHEST_PROTOCOL)


class Multy:

    def __init__(self):
        self.conn = NLP.psycopg2.connect("dbname=postgres user=postgres password=postgres")
        self.filemodelname = './models/multy/multyclassmodel.h5'
        self.tokenizerfilename = './tokenizers/multy/multyclasstokenizer.pickle'
        self.datafilename = 'SELECT * FROM multyclasesset'
        self.recognizeddatafilename = 'SELECT * FROM recognized_multyclass'

    def CreateModel_mul(self, tokenizer, n_clases):
        model = NLP.Sequential()
        optimzer = NLP.Adam(clipvalue=0.5)
        model.add(NLP.Embedding(len(tokenizer.tokenizer.word_index)+1,
                                      EMBEDDING_VECTOR_LENGTH,
                                      input_length=MAX_SEQUENCE_LENGTH, trainable=True))
        model.add(NLP.LSTM(100, dropout=0.2, recurrent_dropout=0.5))
        model.add(NLP.Dense(64, activation="sigmoid"))
        model.add(NLP.Dense(32, activation="sigmoid"))
        model.add(NLP.Dense(16, activation="sigmoid"))
        model.add(NLP.Dense(n_clases, activation='softmax'))
        # compile the model
        model.compile(optimizer=optimzer, loss='categorical_crossentropy', metrics=[
            'categorical_accuracy'])
        return model

    def multyclasstrain(self, mode):

        train = NLP.pd.read_sql(self.datafilename, self.conn)
        train.text = train.text.astype(str)
        recognizedtrain = NLP.pd.read_sql(
            self.recognizeddatafilename, self.conn)
        recognizedtrain.text = recognizedtrain.text.astype(str)
        df = NLP.pd.concat([train, recognizedtrain])
        train = df[~df['questionclass'].isna()]
        train['questionclass'] = train['questionclass'].astype(int)
        train = train.drop_duplicates()
        target = 'questionclass'
        
        showdata(train, target)
        X_train, X_val, y_train, y_val = NLP.train_test_split(
            train, train['questionclass'], test_size=0.2, random_state=64)
        print('Shape of train', X_train.shape)
        print("Shape of Validation ", X_val.shape)

        if(mode == 'evaluate'):
            with open(self.tokenizerfilename,
                      'rb') as handle:
                tokenizer = NLP.p.load(handle)
        else:
            tokenizer = CustomTokenizer(train_texts=X_train['text'])
            # fit o the train
        tokenizer.train_tokenize()
        tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
        tokenized_X_val = tokenizer.vectorize_input(X_val['text'])

        n_clases = 3
        y_trainmatrix = NLP.tensorflow.keras.utils.to_categorical(
            y_train, n_clases)
        y_valmatrix = NLP.tensorflow.keras.utils.to_categorical(
            y_val, n_clases)
        if(mode == 'evaluate'):
            model = NLP.load_model(self.filemodelname)
        else:
            model = self.CreateModel_mul(tokenizer, n_clases)

        history = model.fit(tokenized_X_train, y_trainmatrix,
                            batch_size=64, epochs=2000,
                            validation_data=(tokenized_X_val, y_valmatrix),
                            verbose=2)

        #loss, acc = model.evaluate(tokenized_X_val, y_valmatrix, verbose=2)

        model.save(self.filemodelname)

        with open(self.tokenizerfilename, 'wb') as handle:
            NLP.p.dump(tokenizer, handle,
                             protocol=NLP.p.HIGHEST_PROTOCOL)
