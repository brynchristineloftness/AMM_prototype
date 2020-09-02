import sys
import pandas as pd
import string
import gensim
from gensim.models import Word2Vec 
from gensim.models import Doc2Vec
from gensim.models import CoherenceModel
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from nltk.tokenize import word_tokenize 
import nltk
import xml.etree.ElementTree as ET
import re
import collections
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
from string import digits
from gensim import corpora
import pprint
from gensim import models
from gensim import similarities 
from matplotlib import colors
import numpy as np
from collections import OrderedDict
from xml.etree.ElementTree import XML, fromstring, tostring
from xml.etree.ElementTree import Element, SubElement, Comment
import lxml
import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Masking, Embedding
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
import io
from xml.etree.ElementTree import XML, fromstring
import editdistance
import Levenshtein
import itertools
from functools import reduce
from IPython.display import display, HTML


myfile = pd.read_csv(
    r"C:\Users\brynl\Dropbox\All_Documents\WashingtonStateREU\FilesForModel\OptionBuilder.csv",header = 0)