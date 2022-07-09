import NLP_package



class CustomTokenizer:
    TOP_K = 20000
   
    MAX_SEQUENCE_LENGTH = 33 
    
    def __init__(self, train_texts):
        self.train_texts = train_texts
        self.tokenizer = NLP_package.Tokenizer(num_words=self.TOP_K)

    def train_tokenize(self):
        # Get max sequence length.
        max_length = len(max(self.train_texts, key=len))
        self.max_length = min(max_length, self.MAX_SEQUENCE_LENGTH)

        # Create vocabulary with training texts.
        self.tokenizer.fit_on_texts(self.train_texts)

    def vectorize_input(self, tweets):
        # Vectorize training and validation texts.

        tweets = self.tokenizer.texts_to_sequences(tweets)
        # Fix sequence length to max value. Sequences shorter than the length are
        # padded in the beginning and sequences longer are truncated
        # at the beginning.
        tweets = NLP_package.pad_sequences(
            tweets, maxlen=self.max_length, truncating='post', padding='post')
        return tweets
