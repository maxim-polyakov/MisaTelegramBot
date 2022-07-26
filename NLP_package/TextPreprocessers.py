import NLP_package

class IPreprocessing(NLP_package.ABC):

    @NLP_package.abstractmethod
    def preprocess_text(self, text):
        pass

    @NLP_package.abstractmethod
    def reversepreprocess_text(self, text):
        pass

class Preprocessing(IPreprocessing):

    __mystem = NLP_package.Mystem()

    __russian_stopwords = NLP_package.stopwords.words("russian")
    __english_stopwords = NLP_package.stopwords.words("english")

    __nlp = NLP_package.spacy.load('ru_core_news_md')

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

    @classmethod
    def __remove_punctuation(self, text):
        super().__remove_punctuation()

    @classmethod
    def preprocess_text(self, text):
        try:
            tokens = str(text)
            tokens = super().__mystem.lemmatize(text.lower())
            tokens = [token for token in tokens if token not in super().__russian_stopwords
                      and token != " "
                      and token.strip() not in NLP_package.punctuation]
            tokens = [
                token for token in tokens if token not in super().__english_stopwords]

            text = " ".join(tokens).rstrip('\n')
            pattern3 = r"[\d]"
            pattern2 = "[.]"
            text = NLP_package.re.sub(pattern3, "", text)
            text = NLP_package.re.sub(pattern2, "", text)
            text = self.remove_punctuation(text)
            text = NLP_package.re.sub('  ', ' ', text)
            return text
        except:
            return "except"

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
            tokens = super().__mystem.lemmatize(text.lower())
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
        tokens = super().__mystem.lemmatize(text.lower())
        tokens = [token for token in tokens if token in super().__russian_stopwords
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
            text = super().__remove_punctuation(text)
            tokens = str(text)
            tokens = text.lower().split(' ')
            tokens = [token for token in tokens if token not in super().__russian_stopwords
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