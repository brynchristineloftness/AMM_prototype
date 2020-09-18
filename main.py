#!/usr/bin/python3

#import sys
import pandas as pd
#import string
#import gensim
#from gensim.models import Word2Vec 
#from gensim.models import Doc2Vec
#from gensim.models import CoherenceModel
#from gensim.models import TfidfModel
#from gensim.corpora import Dictionary
#from nltk.tokenize import word_tokenize 
#import nltk
#import xml.etree.ElementTree as ET
#import re
#import collections
#from sklearn.decomposition import PCA
#from matplotlib import pyplot as plt
#from string import digits
#from gensim import corpora
#import pprint
#from gensim import models
#from gensim import similarities 
#from matplotlib import colors
#import numpy as np
#from collections import OrderedDict
#from xml.etree.ElementTree import XML, fromstring, tostring
#from xml.etree.ElementTree import Element, SubElement, Comment
#import lxml
#import keras
#from keras.models import Sequential
#from keras.layers import LSTM, Dense, Dropout, Masking, Embedding
#import tensorflow as tf
#from keras.preprocessing.text import Tokenizer
#import io
#from xml.etree.ElementTree import XML, fromstring
#import itertools
#from functools import reduce
#from IPython.display import display, HTML


def sortstuff(name):
    name = sorted(name)
    for item in range(len(name)):
        name[item] = sorted(name[item])
    name = sorted(name)
    name_set = set(tuple(x) for x in name)
    name = [ list(x) for x in name_set ]
    return name

def defineoracle_optionbuilder():
    oracle = [['testCompleteOption','test02'],['testCompleteOption','test05'],['testCompleteOption','test08'],
          ['testCompleteOption','test19'],['testCompleteOption','test22'], ['testTwoCompleteOptions','test08'],
          ['testTwoCompleteOptions','test19'],['testTwoCompleteOptions','test22'], ['testBaseOptionCharOpt','test08'],
          ['testIllegalOptions', 'test14'],['testSpecialOptChars','test15'],['testCreateIncompleteOption','test16'],
          ['testOptionArgNumbers','test21'],['testCompleteOption','testTwoCompleteOptions'],['testCompleteOption','testBaseOptionCharOpt'],
         ['testBaseOptionCharOpt','testTwoCompleteOptions'],['test02','test05'],['test02','test08'],['test02','test19'],
          ['test02','test22'],['test05','test08'],['test05','test19'],['test05','test22'],['test08','test19'],
          ['test08','test22']]     
    #merges and partial merge oracle       
    mpmoracle = [['testCompleteOption','test02'],['testCompleteOption','test05'],['testCompleteOption','test08'],
          ['testCompleteOption','test19'],['testCompleteOption','test22'], ['testTwoCompleteOptions','test08'],
          ['testTwoCompleteOptions','test19'],['testTwoCompleteOptions','test22'], ['testBaseOptionCharOpt','test08'],
          ['testIllegalOptions', 'test14'],['testSpecialOptChars','test15'],['testCreateIncompleteOption','test16'],
          ['testOptionArgNumbers','test21'], ['testCompleteOption','test06'], ['testCompleteOption','test28'], 
              ['testCompleteOption','test29'],['testTwoCompleteOptions','test28'],['testTwoCompleteOptions','test29'],
              ['testCompleteOption','testTwoCompleteOptions'],['testCompleteOption','testBaseOptionCharOpt'],
         ['testBaseOptionCharOpt','testTwoCompleteOptions'],['test02','test05'],['test02','test08'],['test02','test19'],
          ['test02','test22'],['test05','test08'],['test05','test19'],['test05','test22'],
              ['test08','test19'],['test08','test22'],['test02','test06'],['test02','test28'],['test02','test29'],
              ['test05','test06'],['test05','test28'],['test05','test29'],['test08','test06'],['test08','test28'],['test08','test29'],
              ['test19','test06'],['test19','test28'],['test18','test29'],['test22','test06'],['test22','test28'],['test22','test29']]          
    #sort and get rid of duplicates
    oracle = sortstuff(oracle)
    mpmoracle = sortstuff(mpmoracle)  
    oraclecluster = []        
    for file in oracle:
        oraclecluster.append(file[0])
        oraclecluster.append(file[1])

    oraclecluster = list(dict.fromkeys(oraclecluster))
    mpmoraclecluster = []        
    for file in mpmoracle:
            mpmoraclecluster.append(file[0])
            mpmoraclecluster.append(file[1])
    mpmoraclecluster = list(dict.fromkeys(mpmoraclecluster))
    return oracle, mpmoracle, oraclecluster,mpmoraclecluster

def definetestnames(myfile):     
    x = []
    testlist = myfile['Test'].tolist()
    x = re.compile('test')
    listofnames = []
    for item in testlist: 
        txt = str(item)
        x = re.findall(r"\btest\w+", txt)
        listofnames.append(x)
    myfile['TestName'] = listofnames
    myfile['TestName'] = myfile['TestName'].apply(lambda x:''.join([i for i in x if i not in string.punctuation])) 
    return myfile

def cleaning(myfile):
    myfile = myfile.replace(r'\n',' ', regex=True)    
    myfile['Scenario'] = myfile['Scenario'].apply(
        lambda x:''.join([i for i in x if i not in string.punctuation])) 
    myfile['Test'] = myfile['Test'].apply(lambda x:''.join([i for i in x if i not in string.punctuation]))
    return myfile
    
def camelcasing(myfile):
    myfile['Scenario'] = myfile['Scenario'].apply(lambda x:[i for i in camel_case_split(x)])
    myfile['Scenario'] = myfile['Scenario'].apply(lambda x:' '.join([i for i in x]))
    myfile['Test'] = myfile['Test'].apply(lambda x:[i for i in camel_case_split(x)])
    myfile['Test'] = myfile['Test'].apply(lambda x:' '.join([i for i in x]))
    return myfile

def lowercasing_and_backup(myfile):
    myfile['Test'] = myfile['Test'].apply(lambda x:''.join([i for i in x.lower()])) 
    myfile['Scenario'] = myfile['Scenario'].apply(lambda x:''.join([i for i in x.lower()])) 
    myfile['Combo'] = myfile['Scenario'].str.cat(myfile['Test'],sep = " ")
    myfile.columns = ['Type','Scenario','Test','TestName','Combo']
    mybackupfile = myfile.copy()

def tokenize_and_stopwords(myfile):
    myfile['Scenario'] = myfile.apply(lambda column: nltk.word_tokenize(column['Scenario']),axis = 1)
    myfile['Test'] = myfile.apply(lambda column: nltk.word_tokenize(column['Test']),axis = 1)
    myfile['Combo'] = myfile.apply(lambda column: nltk.word_tokenize(column['Combo']),axis = 1)
    stopwords=['a','an','and','is','of','its','it']
    myfile['Combo']= myfile['Combo'].apply(lambda x: [item for item in x if item not in stopwords])
    return myfile

def tolists(myfile):
    scenariocorpus = myfile['Scenario'].tolist()
    testcorpus = myfile['Test'].tolist()
    combinedcorpus = myfile['Combo'].tolist()   
    return scenariocorpus,testcorpus,combinedcorpus

def textpreprocessing(myfile):
    myfile = cleaning(myfile)
    myfile = definetestnames(myfile)
    myfile = camelcasing(myfile)
    myfile = lowercasing_and_backup(myfile)
    myfile = tokenize_and_stopwords
    scenariocorpus,testcorpus,combinedcorpus = tolists(myfile)
    testlen = len(myfile['Test'])
    return myfile, testlen,scenariocorpus,testcorpus,combinedcorpus

    def main():
        myfile = pd.read_csv(r"OptionBuilder.csv",header = 0)
        oracle, mpmoracle, oraclecluster, mpmoraclecluster = defineoracle_optionbuilder
        myfile,testlen,scenariocorpus,testcorpus,combinedcorpus = textpreprocessing(myfile)
    
    
    main