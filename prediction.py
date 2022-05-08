import libraries
import mapa
from tensorflow.keras.models import load_model


def preprocessing(inpt,prep):
    inp = []
    if(prep == 'qu'):
        for i in inpt:
            inp.append(libraries.specialpreprocess_text(i))
            print(inp)
    elif(prep == 'command'):
        for i in inpt:
            inp.append(libraries.commandpreprocess_text(i))
            print(inp)
    else:
        for i in inpt:
            inp.append(libraries.preprocess_text(i))
            print(inp)
    return inp

def Predict(inpt, tmap, model, tokenizer, prep):
    tmap = tmap
    model = load_model(model)
    inn =[]
    inn.append(preprocessing(inpt,prep).pop())
    #print(inn)
    with open(tokenizer, 'rb') as handle:
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