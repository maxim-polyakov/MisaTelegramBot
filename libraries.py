from keras.layers import Embedding, LSTM, Dense, Dropout, GRU, Input
from keras.models import Sequential

from nltk.corpus import stopwords
import pickle as p
import keras
from keras import backend as K
from keras.preprocessing import text
#from keras.preprocessing import sequence
import requests
import tqdm as tqdm
from string import punctuation
from pymystem3 import Mystem
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.initializers import Constant
from tensorflow.keras.callbacks import EarlyStopping
from tqdm import tqdm
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
import string
#import gensim
import re
import pandas as pd
import tensorflow as tensorflow
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
from collections import Counter
plt.style.use('ggplot')

mystem = Mystem()

TOP_K = 20000
EMBEDDING_VECTOR_LENGTH = 33
MAX_SEQUENCE_LENGTH = 33
russian_stopwords = stopwords.words("russian")
english_stopwords = stopwords.words("english")


class CustomTokenizer:
    def __init__(self, train_texts):
        self.train_texts = train_texts
        self.tokenizer = Tokenizer(num_words=TOP_K)

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
        tweets = pad_sequences(
            tweets, maxlen=self.max_length, truncating='post', padding='post')
        return tweets


def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def preprocess_text(text):
    try:
        tokens = str(text)
        tokens = mystem.lemmatize(text.lower())
        tokens = [token for token in tokens if token not in russian_stopwords
                  and token != " "
                  and token.strip() not in punctuation]
        tokens = [token for token in tokens if token not in english_stopwords]

        text = " ".join(tokens).rstrip('\n')
        pattern3 = r"[\d]"
        pattern2 = "[.]"
        text = re.sub(pattern3, "", text)
        text = re.sub(pattern2, "", text)
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
        text = re.sub(pattern2, "", text)
        text = re.sub(pattern3, "", text)
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
