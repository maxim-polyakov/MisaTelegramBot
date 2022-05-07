import libraries
import mapa
from tensorflow.keras.models import load_model

def Hipredict(inpt):
    tmap = mapa.himapa
    model = load_model('./models/binary/himodel.h5')
    inp = []
    for i in inpt:
        inp.append(libraries.preprocess_text(i))
    inn =[]
    inn.append(inp.pop())
    #print(inn)
    with open('./tokenizers/binary/hitokenizer.pickle', 'rb') as handle:
        tokenizer = libraries.p.load(handle)
    tokenized_inpt = tokenizer.vectorize_input(inn)
    #print(tokenized_inpt)
    score = model.predict(tokenized_inpt)
    outpt = max(libraries.np.round(score).astype(int))
    outscore = max(score)
    return(tmap[outpt[0]])

def QuPpredict(inpt):
    tmap = mapa.qumapa
    model = load_model('./models/binary/qumodel.h5')
    inp = []
    for i in inpt:
        inp.append(libraries.specialpreprocess_text(i))
    print(inp)
    inn =[]
    inn.append(inp.pop())
    #print(inn)
    with open('./tokenizers/binary/qutokenizer.pickle', 'rb') as handle:
        tokenizer = libraries.p.load(handle)
    tokenized_inpt = tokenizer.vectorize_input(inn)


    #print(tokenized_inpt)
    score = model.predict(tokenized_inpt)
    outpt = max(libraries.np.round(score).astype(int))
    outscore = max(score)
    print(outscore)
    return(tmap[outpt[0]])

def ThPpredict(inpt):
    tmap = mapa.thmapa
    model = load_model('./models/binary/thmodel.h5')
    inp = []
    for i in inpt:
        inp.append(libraries.specialpreprocess_text(i))
    print(inp)
    inn =[]
    inn.append(inp.pop())
    #print(inn)
    with open('./tokenizers/binary/thtokenizer.pickle', 'rb') as handle:
        tokenizer = libraries.p.load(handle)
    tokenized_inpt = tokenizer.vectorize_input(inn)


    #print(tokenized_inpt)
    score = model.predict(tokenized_inpt)
    outpt = max(libraries.np.round(score).astype(int))
    outscore = max(score)
    print(outscore)
    return(tmap[outpt[0]])


def MultyPpredict(inpt):
    tmap = mapa.multymapa
    model = load_model('./models/multy/multyclassmodel.h5')
    inp = []
    for i in inpt:
        inp.append(libraries.preprocess_text(i))
    print(inp)
    inn =[]
    inn.append(inp.pop())
    with open('./tokenizers/multy/multyclasstokenizer.pickle', 'rb') as handle:
        tokenizer = libraries.p.load(handle)
    tokenized_inpt = tokenizer.vectorize_input(inn)
    scoreplu = model.predict(tokenized_inpt)
    outpt = mapa.multymapa[scoreplu.argmax(axis=-1)[0]]
    print(outpt)
    return outpt