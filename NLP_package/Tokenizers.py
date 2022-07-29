import NLP_package

class ITokenizer(NLP_package.ABC):

    @NLP_package.abstractmethod
    def train_tokenize(self):
        pass

    @NLP_package.abstractmethod
    def vectorize_input(self, tweets):
        pass


class CustomTokenizer(ITokenizer):
    TOP_K = 20000

    MAX_SEQUENCE_LENGTH = 33
    tokenizer = NLP_package.Tokenizer(num_words=TOP_K)
    train_texts = str(object)
    word_index = 0
    def __init__(self, train_texts):
        self.train_texts = train_texts

    @classmethod
    def train_tokenize(self):
        max_length = len(max(self.train_texts, key=len))
        self.max_length = min(max_length, self.MAX_SEQUENCE_LENGTH)
        self.tokenizer.fit_on_texts(self.train_texts)
        self.word_index = self.tokenizer.word_index

    @classmethod
    def vectorize_input(self, tweets):
        tweets = self.tokenizer.texts_to_sequences(tweets)
        tweets = NLP_package.pad_sequences(
            tweets, maxlen=self.max_length, truncating='post', padding='post')
        return tweets
