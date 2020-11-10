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
import functions
import setfile
import clean
import parse
import pack_n_prunes
import checks



main():
    oracle, mpmoracle = defineoracles()
    myfile = definefile()
    oraclecluster, mpmoraclecluster = cleanoracles(oracle,mpmoracle)
    myfile,mybackupfile = cleanfile(myfile)
    myfile,scenariocorpus,testcorpus,combinedcorpus,testlen = preprocess(myfile)
    defaultgrid = [[0 for i in range(testlen)] for j in range(testlen)]
    autotree, autoroot, manualtree, manualroot,cleanautotree,cleanautoroot,cleanmanualtree,cleanmanualroot = setparsefile()
    cleanautoroot,cleanmanualroot = cleanparsefiles(cleanautoroot,cleanmanualroot)
    myfile,listofallfiles = addxmltofile(myfile,cleanmanualroot,cleanautoroot)
    myfile = isolatemethods_asserts(myfile,listofallfiles)
    myfile = cleancolumns(myfile)
    pack3, prune1,prune3,prune4,prunepack= makepacksandprunes(myfile,testlen)
    manuallist,autolist = defineAutoandManual(myfile)
    round1,keep_pack = round1func(myfile,testlen,autolist,manuallist)
    round2,round3,round4, keep_pack = round2func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack)
    round3, keep_pack = round3func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,round3)
    round4, round5, keep_pack = round4func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,round4)
    round5, keep_pack = round5func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,round5)
    round6, keep_pack = round6func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack)
    defineTest(keep_pack,oracle,mpmoracle)
