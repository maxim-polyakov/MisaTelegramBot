
from tensorflow.keras.models import load_model
import psycopg2


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
from NLP import *
plt.style.use('ggplot')

