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



main():
    oracle, mpmoracle = defineoracles()
    myfile = definefile()
    oraclecluster, mpmoraclecluster = cleanoracles(oracle,mpmoracle)
    myfile,mybackupfile = cleanfile(myfile)
    myfile,scenariocorpus,testcorpus,combinedcorpus,testlen = preprocess(myfile)
    autotree, autoroot, manualtree, manualroot,cleanautotree,cleanautoroot,cleanmanualtree,cleanmanualroot = setparsefile()
    cleanautoroot,cleanmanualroot = cleanparsefiles(cleanautoroot,cleanmanualroot)
    myfile,listofallfiles = addxmltofile(myfile,cleanmanualroot,cleanautoroot)
    myfile = isolatemethods_asserts(myfile,listofallfiles)

    







clean('Methods')
clean('Asserts')
clean('Methods_Asserts')
clean('Assert_Only')
    
for file in range(len(myfile['Asserts'])):
    myfile['Asserts'][file] = myfile['Asserts'][file].split()
for file in range(len(myfile['Methods'])):
    myfile['Methods'][file] = myfile['Methods'][file].split()
for file in range(len(myfile['Methods_Asserts'])):
    myfile['Methods_Asserts'][file] = myfile['Methods_Asserts'][file].split()
for file in range(len(myfile['Assert_Only'])):
    myfile['Assert_Only'][file] = myfile['Assert_Only'][file].split()
    
    

pack3 = one_2_one_asserts(myfile,testlen)
prune1 = scenariomodel(myfile,testlen)
prune3 = tfidf_model(myfile,testlen,.84,'bnn')
prune4 = lsi_prune(myfile)
prunepack = prune1 + prune3+prune4
prunepack= sortstuff(prunepack)

manuallist = []
autolist = []

for item in range(len(myfile['Type'])):
    if myfile['Type'][item] == "Manual":
        manuallist.append(myfile['TestName'][item])
    else:
        autolist.append(myfile['TestName'][item])


keep_pack = []

#---------------
round3 = longest_common_subsequence(myfile,testlen,4)
round3 = sortstuff(round3)
round3real = []
for item in round3:
    if item[0] in autolist and item[1] in manuallist:
        round3real.append(item)
round3 = round3real

print('three',len(round3),1)
prototypecheck(round3)
keep_pack += round3
#-------
round4 = setmetrics_combo(myfile,testlen,defaultgrid,"Combo",.51)
round4 = sortstuff(round4)
round4real = []
for item in round4:
    if item[0] in autolist and item[1] in manuallist:
        round4real.append(item)
round4 = round4real
#round4 = [x for x in round4 if x not in round3]

prune_scenario = setmetrics_combo(myfile,testlen,defaultgrid,"Scenario",.7889)
#branch decision tree
round1 = [x for x in round4 if x in prune_scenario]
round4 = [x for x in round4 if x not in prune_scenario]

prune_asserts = setmetrics_combo(myfile,testlen,defaultgrid,"Asserts",.35)
round4 = [x for x in round4 if x not in prune_asserts]

prune_asserts = setmetrics_combo(myfile,testlen,defaultgrid,"Methods_Asserts",.68)
#branch decision tree
round6 = [x for x in round4 if x not in prune_asserts]
round4 = [x for x in round4 if x in prune_asserts]


split = tfidf_model(myfile,testlen,.65,'bnn')
round4 = [x for x in round4 if x in split]

print('four',len(round4),2) 
prototypecheck(round4)
keep_pack+=round4
#-------------
round1 = sortstuff(round1)
round1 = [x for x in round1 if x not in prunepack]

prune_asserts = setmetrics_combo(myfile,testlen,defaultgrid,"Methods_Asserts",.9999)
round1 = [x for x in round1 if x in prune_asserts]


split = tfidf_model(myfile,testlen,.785,'bnn')
round1 = [x for x in round1 if x in split]

print('one',len(round1),2) 
prototypecheck(round1)
keep_pack+=round1
#----------------------------

round6 = sortstuff(round6)

add_methods = setmetrics_combo(myfile,testlen,defaultgrid,"Methods",.9995)
round7 = [x for x in round6 if x in add_methods]
round6 = [x for x in round6 if x not in add_methods]

prune_scenario = setmetrics_combo(myfile,testlen,defaultgrid,"Scenario",.7)
round6 = [x for x in round6 if x not in prune_scenario]

split = tfidf_model(myfile,testlen,.605,'bnn')
round6 = [x for x in round6 if x not in split]

round6 = [x for x in round6 if x not in prunepack]

print('six',len(round6),2)
prototypecheck(round6)
keep_pack+=round6
#-----------
round7 = sortstuff(round7)

prune_scenario = setmetrics_combo(myfile,testlen,defaultgrid,"Scenario",.69)
round7 = [x for x in round7 if x not in prune_scenario]

prune_scenario = setmetrics_combo(myfile,testlen,defaultgrid,"Combo",.59)
round7 = [x for x in round7 if x not in prune_scenario]


split = tfidf_model(myfile,testlen,.58,'bnn')
round7 = [x for x in round7 if x not in split]

round7 = [x for x in round7 if x not in prunepack]

print('seven',len(round7),3)
prototypecheck(round7)
keep_pack+=round7
#----------------------------
add_methods = setmetrics_combo(myfile,testlen,defaultgrid,"Methods_Asserts",.65)
round8 = [x for x in round7 if x in add_methods]

prune_scenario = setmetrics_combo(myfile,testlen,defaultgrid,"Combo",.4)
round8 = [x for x in round8 if x in prune_scenario]

split = tfidf_model(myfile,testlen,.58,'bnn')
round8 = [x for x in round8 if x not in split]

round8 = [x for x in round8 if x not in prunepack]
print('eight',len(round8),2)
prototypecheck(round8)
keep_pack+=round8
#+++++++++++++++++++++++++

epic1 = keep_pack

print(len(epic1))
counter = 0
count = 0
counter2 = 0
for item in sorted(epic1):
    if item in oracle :
        print('*o*',end='')
        counter+=1
    if item in mpmoracle:
        print("*mpm*",end = '')
        counter2+=1
    print (item,end = '')
    if item in round1:
        print('r1')
    elif item in round3:
        print('r3')
    elif item in round4:
        print('r4')
    elif item in round6:
        print('r6')
    elif item in round7 :
        print('r7')
    elif item in round9:
        print('r9')

    count+=1
print("found in oracle: ",counter,'out of',len(oracle))
print("found in mpm: ",counter2,'out of',len(mpmoracle))

print('number of matches',len(epic1))
