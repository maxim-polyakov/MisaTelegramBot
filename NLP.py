import libraries
import mapa

def DataCleaner(filename, string):
    train = libraries.pd.read_excel(filename)
    train.text=train.text.astype(str)
    df=libraries.pd.concat([train])
    df['text'] = df['text'].apply(libraries.preprocess_text)
    train= df[~df[string].isna()]
    train[string] = train[string].astype(int)
    train.to_excel(filename,index=False)

def QuestionsetCleaner(filename):
    
    train = libraries.pd.read_excel(filename)
    train.text=train.text.astype(str)
    df=libraries.pd.concat([train])
    df['text'] = df['text'].apply(libraries.specialpreprocess_text)
    train= df[~df['question'].isna()]
    train['question'] = train['question'].astype(int)
    train.to_excel('./datasets/questionset.xlsx',index=False)


def CreateModel_bin(tokenizer):
    optimzer=libraries.Adam(clipvalue=0.5)
    model=libraries.Sequential()
    model.add(libraries.Embedding(len(tokenizer.tokenizer.word_index)+1, libraries.EMBEDDING_VECTOR_LENGTH, input_length=libraries.MAX_SEQUENCE_LENGTH,trainable=True,mask_zero=True))
    model.add(libraries.Dropout(0.1))
    model.add(libraries.LSTM(64))
    model.add(libraries.Dense(64, activation="relu"))
    model.add(libraries.Dense(32, activation="relu"))
    model.add(libraries.Dense(16, activation="relu"))
    model.add(libraries.Dense(1, activation='sigmoid'))
    # compile the model
    model.compile(optimizer=optimzer, loss='binary_crossentropy', metrics=['binary_accuracy'])
    
    return model
    
def CreateModel_mul(tokenizer,n_clases):
    model=libraries.Sequential()
    optimzer=libraries.Adam(clipvalue=0.5)
    model.add(libraries.Embedding(len(tokenizer.tokenizer.word_index)+1, libraries.EMBEDDING_VECTOR_LENGTH, input_length=libraries.MAX_SEQUENCE_LENGTH,trainable=True))
    model.add(libraries.Dropout(0.1))
    model.add(libraries.LSTM(64, dropout=0.2, recurrent_dropout=0.5))
    model.add(libraries.Dense(64, activation="softmax"))
    model.add(libraries.Dense(32, activation="softmax"))
    model.add(libraries.Dense(16, activation="softmax"))
    model.add(libraries.Dense(n_clases,activation='softmax'))
    # compile the model
    model.compile(optimizer=optimzer, loss='categorical_crossentropy', metrics=['categorical_accuracy'])
    
    return model

def ishitrain():
        
    train = libraries.pd.read_excel('./datasets/dataset.xlsx')
    test = libraries.pd.read_excel('./validset/validset.xlsx')
    train.text=train.text.astype(str)

    df=libraries.pd.concat([train])
    df1=libraries.pd.concat([test])
    
    train= df[~df['hi'].isna()]
    train['hi'] = train['hi'].astype(int)
    test = df1[~df1['text'].isna()]
    train = train.drop_duplicates()
    test = train.drop_duplicates()
    X_train, X_val, y_train, y_val = libraries.train_test_split(train, train['hi'], test_size=0.3, random_state=42)
    print('Shape of train',X_train.shape)
    print("Shape of Validation ",X_val.shape)
    
    tokenizer = libraries.CustomTokenizer(train_texts = X_train['text'])
    # fit o the train
    tokenizer.train_tokenize()
    tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
    tokenized_X_val = tokenizer.vectorize_input(X_val['text'])
    
    model = CreateModel_bin(tokenizer)  
    
    history=model.fit( tokenized_X_train, y_train,
                      validation_data=(tokenized_X_val, y_val),
                      batch_size=512,
                      epochs=2000,
                      verbose=2, # hide the output because we have so many epochs
                      )
    
    model.save('./models/binary/himodel.h5')
    
    with open('./tokenizers/binary/hitokenizer.pickle', 'wb') as handle:
        libraries.p.dump(tokenizer, handle, protocol=libraries.p.HIGHEST_PROTOCOL)
        
def isqutrain():
    
    train = libraries.pd.read_excel('./datasets/questionset.xlsx')
    train.text=train.text.astype(str)
    df=libraries.pd.concat([train])   
    train= df[~df['question'].isna()]
    train['question'] = train['question'].astype(int)
    train = train.drop_duplicates()
    
    X_train, X_val, y_train, y_val = libraries.train_test_split(train, train['question'], test_size=0.2, random_state=64)
    print('Shape of train',X_train.shape)
    print("Shape of Validation ",X_val.shape)
    tokenizer = libraries.CustomTokenizer(train_texts = X_train['text'])
    # fit o the train
    tokenizer.train_tokenize()
    tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
    tokenized_X_val = tokenizer.vectorize_input(X_val['text'])
    
    model = CreateModel_bin(tokenizer)

    history=model.fit( tokenized_X_train, y_train,
                      validation_data=(tokenized_X_val, y_val),
                      batch_size=64,
                      epochs=300,
                      verbose=2,
                      )
    
    model.save('./models/binary/qumodel.h5')
    
    with open('./tokenizers/binary/qutokenizer.pickle', 'wb') as handle:
        libraries.p.dump(tokenizer, handle, protocol=libraries.p.HIGHEST_PROTOCOL)
    
def thtrain():
    
    train = libraries.pd.read_excel('./datasets/thanksset.xlsx')
    train.text=train.text.astype(str)
    df=libraries.pd.concat([train])   
    train= df[~df['thanks'].isna()]
    train['thanks'] = train['thanks'].astype(int)
    train = train.drop_duplicates()
    
    X_train, X_val, y_train, y_val = libraries.train_test_split(train, train['thanks'], test_size=0.2, random_state=64)
    print('Shape of train',X_train.shape)
    print("Shape of Validation ",X_val.shape)
    tokenizer = libraries.CustomTokenizer(train_texts = X_train['text'])
    # fit o the train
    tokenizer.train_tokenize()
    tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
    tokenized_X_val = tokenizer.vectorize_input(X_val['text'])
    
    model = CreateModel_bin(tokenizer)
    
    
    history=model.fit( tokenized_X_train, y_train,
                      validation_data=(tokenized_X_val, y_val),
                      batch_size=64,
                      epochs=300,
                      verbose=2,
                      )
    
    model.save('./models/binary/thmodel.h5')
    
    with open('./tokenizers/binary/thtokenizer.pickle', 'wb') as handle:
        libraries.p.dump(tokenizer, handle, protocol=libraries.p.HIGHEST_PROTOCOL)    



def multyclasstrain():
    
    train = libraries.pd.read_excel('./datasets/multyclasesset.xlsx')
    train.text=train.text.astype(str)
    df=libraries.pd.concat([train])   
    train= df[~df['questionclass'].isna()]
    train['questionclass'] = train['questionclass'].astype(int)
    train = train.drop_duplicates()
    
    X_train, X_val, y_train, y_val = libraries.train_test_split(train, train['questionclass'], test_size=0.2, random_state=64)
    print('Shape of train',X_train.shape)
    print("Shape of Validation ",X_val.shape)
    tokenizer = libraries.CustomTokenizer(train_texts = X_train['text'])
    # fit o the train
    tokenizer.train_tokenize()
    tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
    tokenized_X_val = tokenizer.vectorize_input(X_val['text'])
    
    n_clases = 3
    y_trainmatrix = libraries.tensorflow.keras.utils.to_categorical(y_train, n_clases)
    y_valmatrix = libraries.tensorflow.keras.utils.to_categorical(y_val, n_clases)
    
    model = CreateModel_mul(tokenizer,n_clases)
    
    
    history=model.fit(tokenized_X_train, y_trainmatrix, 
                  batch_size=64, epochs=600, 
                  validation_data=(tokenized_X_val,y_valmatrix), 
                  verbose=2)
    
    #loss, acc = model.evaluate(tokenized_X_val, y_valmatrix, verbose=2)
    
    model.save('./models/multy/multyclassmodel.h5')
    
    with open('./tokenizers/multy/multyclasstokenizer.pickle', 'wb') as handle:
        libraries.p.dump(tokenizer, handle, protocol=libraries.p.HIGHEST_PROTOCOL)
    
    