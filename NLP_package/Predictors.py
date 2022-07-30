import NLP_package

class IPredictor(NLP_package.ABC):

    @NLP_package.abstractmethod
    def predict(self):
        pass

class Binary(IPredictor):

    @classmethod
    def __preprocessing(self, inpt, prep):

        inp = []
        if(prep == 'qu'):
            for i in inpt:
                pr = NLP_package.TextPreprocessers.QuestionPreprocessing()
                inp.append(pr.preprocess_text(i))
               # print(self.inp)
        elif(prep == 'command'):
            for i in inpt:
                pr = NLP_package.TextPreprocessers.CommandPreprocessing()
                inp.append(pr.preprocess_text(i))
             #   print(self.inp)
        else:
            for i in inpt:
                pr = NLP_package.TextPreprocessers.CommonPreprocessing()
                inp.append(pr.preprocess_text(i))
            #    print(self.inp)
        return inp

    @classmethod
    def predict(self, inpt, tmap, model, tokenizer, prep):
        model = NLP_package.load_model(model)
        inn = []
        inn.append(self.__preprocessing(inpt, prep).pop())
        #print(inn)
        with open(tokenizer, 'rb') as handle:
            tokenizer = NLP_package.p.load(handle)
            tokenized_inpt = tokenizer.vectorize_input(inn)

        #print(tokenized_inpt)
        score = model.predict(tokenized_inpt)
        outpt = max(NLP_package.np.round(score).astype(int))
        outscore = max(score)
        print(outscore)
        return(tmap[outpt[0]])

class NonNeuro(Binary):

    @classmethod
    def __preprocessing(self, inpt, prep):
        super().__preprocessing(inpt,prep)

    @classmethod
    def predict(self, inpt, tmap, model, tokenizer, prep):
        with open(model, 'rb') as handle:
            model = NLP_package.p.load(handle)

        inn = []
        inn.append(self.__preprocessing(inpt, prep).pop())

        pr = NLP_package.TextPreprocessers.CommonPreprocessing()

        with open(tokenizer, 'rb') as handle:
            tokenizer = NLP_package.p.load(handle)
            tokenized_inpt = tokenizer.transform(inn).toarray()
            nb_x_test = tokenizer.transform(inn).toarray()

        score = model.predict_proba(tokenized_inpt)

        return(tmap[score.argmax(axis=-1)[0]])


class Multy(IPredictor):

    @classmethod
    def predict(self, inpt, tmap, model, tokenizer):
        model = NLP_package.load_model(model)
        self.inp = []
        pr = NLP_package.TextPreprocessers.CommonPreprocessing()
        for i in inpt:
            self.inp.append(pr.preprocess_text(i))
        #    print(self.inp)
            inn = []
            inn.append(self.inp.pop())
        with open(tokenizer, 'rb') as handle:
            tokenizer = NLP_package.p.load(handle)
        tokenized_inpt = tokenizer.vectorize_input(inn)
        scoreplu = model.predict(tokenized_inpt)
        outpt = tmap[scoreplu.argmax(axis=-1)[0]]
      #  print(outpt)
        self.inp = []
        return outpt