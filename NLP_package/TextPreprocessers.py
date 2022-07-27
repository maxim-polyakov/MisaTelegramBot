import NLP_package

class IPreprocessing(NLP_package.ABC):

    @NLP_package.abstractmethod
    def preprocess_text(self, text):
        pass

    @NLP_package.abstractmethod
    def reversepreprocess_text(self, text):
        pass

class Preprocessing(IPreprocessing):
    _mystem = NLP_package.Mystem()

    _russian_stopwords = NLP_package.stopwords.words("russian")

    _english_stopwords = NLP_package.stopwords.words("english")

    _nlp = NLP_package.spacy.load('ru_core_news_md')



    @property
    def mystem(self):
        return self.__mystem

    @property
    def russian_stopwords(self):
        return self.__russian_stopwords

    @property
    def english_stopwords(self):
        return self.__english_stopwords

    @property
    def nlp(self):
        return self.__nlp


    @classmethod
    def __remove_punctuation(self, text):
        translator = str.maketrans('', '', NLP_package.string.punctuation)
        return text.translate(translator)

    @classmethod
    def preprocess_text(self, text):
        try:
            tokens = text.lower().split(' ')
            tokens = [token for token in tokens if token not in self.__russian_stopwords
                      and token != " "
                      and token.strip() not in NLP_package.punctuation]
        
       # text = self.remove_punctuation(text)
            text = " ".join(tokens).rstrip('\n')
            text = text.replace('  ', ' ')
            return text
        except:
            return "except"

    @classmethod
    def reversepreprocess_text(self,text):
        super().reversepreprocess_text()


class CommonPreprocessing(Preprocessing):

    def __init__(self):
        super(CommonPreprocessing, self).__init__()
    @classmethod
    def __remove_punctuation(self, text):
        super().__remove_punctuation()

    @classmethod
    def preprocess_text(self, text):

        tokens = str(text)
        mystem = super(CommonPreprocessing, self).__mystem
        tokens = mystem.lemmatize(text.lower())
        print(tokens)
        tokens = [token for token in tokens if token not in super(CommonPreprocessing, self).__russian_stopwords
                    and token != " "
                    and token.strip() not in NLP_package.punctuation]
        tokens = [
            token for token in tokens if token not in super(CommonPreprocessing, self).__english_stopwords]

        text = " ".join(tokens).rstrip('\n')
        pattern3 = r"[\d]"
        pattern2 = "[.]"
        text = NLP_package.re.sub(pattern3, "", text)
        text = NLP_package.re.sub(pattern2, "", text)
        text = self.remove_punctuation(text)
        text = NLP_package.re.sub('  ', ' ', text)
        return text


    @classmethod
    def reversepreprocess_text(self, text):
        super().reversepreprocess_text()


class QuestionPreprocessing(Preprocessing):

    @classmethod
    def __remove_punctuation(self, text):
        super().reversepreprocess_text()

    @classmethod
    def preprocess_text(self, text):
        try:
            tokens = str(text).split(' ')
            tokens = super().mystem.lemmatize(text.lower())
            tokens = [token for token in tokens if token != " "]
        
       # text = self.remove_punctuation(text)
            text = " ".join(tokens).rstrip('\n')
            text = NLP_package.re.sub('[!@#$-><%^&*()_=+/\|:;~,.]', '', text)
            text = NLP_package.re.sub('  ', ' ', text)
            text = text.replace(' ? ', '?')

            return text
        except:
            return "except"

    @classmethod
    def reversepreprocess_text(self, text):
        tokens = str(text)
        tokens = super().mystem.lemmatize(text.lower())
        tokens = [token for token in tokens if token in super().russian_stopwords
                      and (token != " " or token == "?")]
        text = " ".join(tokens).rstrip('\n')
        #text = remove_punctuation(text)
        text = NLP_package.re.sub('  ', ' ', text)
        return text


class CommandPreprocessing(Preprocessing):

    @classmethod
    def __remove_punctuation(self, text):
        super().__remove_punctuation()

    @classmethod
    def preprocess_text(self, text):
        try:
            text = self.__remove_punctuation(text)
            tokens = str(text)
            tokens = text.lower().split(' ')
            tokens = [token for token in tokens if token not in super().russian_stopwords
                      and token != " "
                      and token.strip() not in NLP_package.punctuation]
            text = " ".join(tokens).rstrip('\n')
            return text
        except:
            return "except"

    @classmethod
    def reversepreprocess_text(self, text):
        document = self.nlp(text)
        tokens = [token.lemma_ for token in document if token.pos_ == 'VERB']
        
       # text = self.remove_punctuation(text)
        text = " ".join(tokens).rstrip('\n')
        print(text)
        return text