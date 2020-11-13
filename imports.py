import pandas as pd
import string
import gensim
from gensim.models import Word2Vec 
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
from nltk.tokenize import word_tokenize 
import nltk
import xml.etree.ElementTree as ET
import re
import collections
from gensim import models
from gensim import similarities 
from IPython.display import display, HTML
from functions import *
from setfile import *
from clean import *
from parse import *
from pack_n_prunes import *
from checks import *