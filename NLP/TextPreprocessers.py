import NLP


class Preprocessing:

    mystem = NLP.Mystem()

    russian_stopwords = NLP.stopwords.words("russian")
    english_stopwords = NLP.stopwords.words("english")

    def __init__(self):
        pass

    def remove_punctuation(self, text):

        translator = str.maketrans('', '', NLP.string.punctuation)
        return text.translate(translator)

    def preprocess_text(self, text):
        try:
            tokens = str(text)
            tokens = text.lower().split(' ')
            tokens = [token for token in tokens if token not in self.russian_stopwords
                     and token != " "]
        
       # text = self.remove_punctuation(text)
            text = " ".join(tokens).rstrip('\n')
            return text
        except:
            return "except"


class CommonPreprocessing(Preprocessing):

    def __init__(self):
        pass

    def preprocess_text(self, text):
        try:
            tokens = str(text)
            tokens = self.mystem.lemmatize(text.lower())
            tokens = [token for token in tokens if token not in self.russian_stopwords
                      and token != " "
                      and token.strip() not in NLP.punctuation]
            tokens = [
                token for token in tokens if token not in self.english_stopwords]

            text = " ".join(tokens).rstrip('\n')
            pattern3 = r"[\d]"
            pattern2 = "[.]"
            text = NLP.re.sub(pattern3, "", text)
            text = NLP.re.sub(pattern2, "", text)
            text = self.remove_punctuation(text)
            text = NLP.re.sub('  ', ' ', text)
            return text
        except:
            return "except"


class QuestionPreprocessing(Preprocessing):

    def __init__(self):
        pass

    def preprocess_text(self, text):

        tokens = str(text).split(' ')
        tokens = self.mystem.lemmatize(text.lower())
        tokens = [token for token in tokens if token != " "]
        
       # text = self.remove_punctuation(text)
        text = " ".join(tokens).rstrip('\n')
        text = NLP.re.sub('[!@#$-><%^&*()_=+/\|:;~,.]', '', text)
        text = NLP.re.sub('  ', ' ', text)
        text = text.replace(' ? ', '?')

        return text
 # №       try:
  # №     except:
  #          return "except"


class CommandPreprocessing(Preprocessing):

    def __init__(self):
        pass

    def preprocess_text(self, text):
        try:
            text = self.remove_punctuation(text)
            tokens = str(text)
            tokens = text.lower().split(' ')
            tokens = [token for token in tokens if token not in self.russian_stopwords
                     and token != " "
                     and token.strip() not in NLP.punctuation]
        
       # text = self.remove_punctuation(text)
            text = " ".join(tokens).rstrip('\n')
            return text
        except:
            return "except"
