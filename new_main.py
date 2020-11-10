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

myfile = pd.read_csv(
    r"OptionBuilder.csv",header = 0)

oracle = [['testCompleteOption','test02'],['testCompleteOption','test05'],['testCompleteOption','test08'],
          ['testCompleteOption','test19'],['testCompleteOption','test22'], ['testTwoCompleteOptions','test08'],
          ['testTwoCompleteOptions','test19'],['testTwoCompleteOptions','test22'], ['testBaseOptionCharOpt','test08'],
          ['testIllegalOptions', 'test14'],['testSpecialOptChars','test15'],['testCreateIncompleteOption','test16'],
          ['testOptionArgNumbers','test21']]
          
#merges and partial merge oracle       
mpmoracle = [['testCompleteOption','test02'],['testCompleteOption','test05'],['testCompleteOption','test08'],
          ['testCompleteOption','test19'],['testCompleteOption','test22'], ['testTwoCompleteOptions','test08'],
          ['testTwoCompleteOptions','test19'],['testTwoCompleteOptions','test22'], ['testBaseOptionCharOpt','test08'],
          ['testIllegalOptions', 'test14'],['testSpecialOptChars','test15'],['testCreateIncompleteOption','test16'],
          ['testOptionArgNumbers','test21'], ['testCompleteOption','test06'], ['testCompleteOption','test28'], 
              ['testCompleteOption','test29'],['testTwoCompleteOptions','test28'],['testTwoCompleteOptions','test29']]          

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

#gets rid of new lines in strings for whole file
myfile = myfile.replace(r'\n',' ', regex=True) 

#gets rid of punct in scenarios
myfile['Scenario'] = myfile['Scenario'].apply(
    lambda x:''.join([i for i in x if i not in string.punctuation])) 

#gets rid of punct in tests and replaces with space
myfile['Test'] = myfile['Test'].apply(lambda x:''.join([i for i in x if i not in string.punctuation]))

#isolating test names and putting into column
x = []
testlist = myfile['Test'].tolist()
x = re.compile('test')
listofnames = []
newlist = []

#define test name list
for item in testlist: 
    txt = str(item)
    x = re.findall(r"\btest\w+", txt)
    listofnames.append(x)

myfile['TestName'] = listofnames

#gets rid of punctuation in Test Name Column
myfile['TestName'] = myfile['TestName'].apply(lambda x:''.join([i for i in x if i not in string.punctuation])) 

#separating camelcasing in scenarios and tests

myfile['Scenario'] = myfile['Scenario'].apply(lambda x:[i for i in camel_case_split(x)])
myfile['Scenario'] = myfile['Scenario'].apply(lambda x:' '.join([i for i in x]))
myfile['Test'] = myfile['Test'].apply(lambda x:[i for i in camel_case_split(x)])
myfile['Test'] = myfile['Test'].apply(lambda x:' '.join([i for i in x]))

#makes all lowercase
myfile['Test'] = myfile['Test'].apply(lambda x:''.join([i for i in x.lower()])) 
myfile['Scenario'] = myfile['Scenario'].apply(lambda x:''.join([i for i in x.lower()])) 

#creating new column with combined scenario and test words

myfile['Combo'] = myfile['Scenario'].str.cat(myfile['Test'],sep = " ")
myfile.columns = ['Type','Scenario','Test','TestName','Combo']

#making a backup file of cleaned, untokenized information
mybackupfile = myfile.copy()

    #preprocessing by tokenizing...
    
#Tokenizes using NLTK the Scenario column
myfile['Scenario'] = myfile.apply(lambda column: nltk.word_tokenize(column['Scenario']),axis = 1)
#tokenizes using NLTK the Test column
myfile['Test'] = myfile.apply(lambda column: nltk.word_tokenize(column['Test']),axis = 1)
#tokenizes using NLTK the Combo column
myfile['Combo'] =myfile.apply(lambda column: nltk.word_tokenize(column['Combo']),axis = 1)

#removing stopwords from combo
stopwords=['a','an','and','is','of','its','it']
myfile['Combo']= myfile['Combo'].apply(lambda x: [item for item in x if item not in stopwords])

    #create corpora in lists
scenariocorpus = myfile['Scenario'].tolist()
testcorpus = myfile['Test'].tolist()
combinedcorpus = myfile['Combo'].tolist()

#defining unique word count for corpus lists
wordcountscenario = collections.defaultdict(int)
wordcounttest = collections.defaultdict(int)
wordcountcombined = collections.defaultdict(int)

#declaring testlen variable (how many tests)
testlen = len(myfile['Test'])

#getting stuff for figures ready
defaultgrid = [[0 for i in range(testlen)] for j in range(testlen)]



    #using srcml for code analysis....
#used srcml to produce xml files for original java test files
autotree = ET.parse(r'OptionBuilder_ESTest.xml')
autoroot = autotree.getroot()
manualtree = ET.parse(r'OptionBuilderTest.xml')
manualroot = manualtree.getroot()
#removed all leading comments before declaration of package in original java files
#used srcml to produce xml files for new clean java test files
cleanautotree = ET.parse(r'cleanautotests.xml')
cleanautoroot = cleanautotree.getroot()
cleanmanualtree = ET.parse(r'cleanmanualtests.xml')
cleanmanualroot = cleanmanualtree.getroot()


#gets rid of wonky formatting that includes link to srcml for auto and manual trees
for child in cleanautoroot:
    child.tag = child.tag.replace('{http://www.srcML.org/srcML/src}','')
    child.tag = child.tag.replace('class','startclass')
    #print(child.tag,child.attrib)
#print()
for child in cleanmanualroot:
    child.tag = child.tag.replace('{http://www.srcML.org/srcML/src}','')
    child.tag = child.tag.replace('class','startclass')
    #print(child.tag,child.attrib)
    
for tags in cleanautoroot.iter():
    tags.tag = tags.tag.replace('{http://www.srcML.org/srcML/src}','')

for tags in cleanmanualroot.iter():
    tags.tag = tags.tag.replace('{http://www.srcML.org/srcML/src}','')
    
listofmanualfiles = []
startclassElement = cleanmanualroot.find('startclass/block')
for element in startclassElement: #isolates comment, function, comment, function for all 
    if (element.tag != 'comment'): #isolates only function blocks
        listofmanualfiles.append(ET.tostring(element, encoding='unicode')) 

listofautofiles = []
startclassElement = cleanautoroot.find('startclass/block')
for element in startclassElement: #isolates comment, function, comment, function for all 
    if (element.tag != 'comment'): #isolates only function blocks
        listofautofiles.append(ET.tostring(element, encoding='unicode')) 

listofallfiles = []
listofallfiles = listofmanualfiles + listofautofiles

#creating uncleaned XML column
myfile['XML'] = ['' for x in range(len(myfile['Combo']))]
myfile.columns = ['Type','Scenario','Test','TestName','Combo','XML']
myfile['XML'] = listofallfiles

#get rid of keywords
myfile['XML'] = [entry.replace('4000','') for entry in myfile['XML']]

#place new root
for file in range(len(myfile['XML'])):
    myfile['XML'][file] = '<root>' + myfile['XML'][file] + '</root>'
    
for file in range(len(listofmanualfiles)):
    listofmanualfiles[file] = '<root>' + listofmanualfiles[file] + '</root>'
    
for file in range(len(listofautofiles)):
    listofautofiles[file] = '<root>' + listofautofiles[file] + '</root>'
    
for file in range(len(listofallfiles)):
    listofallfiles[file] = '<root>' + listofallfiles[file] + '</root>'

myfile['XML'] = [entry.replace(r'\n','') for entry in myfile['XML']]


#creating uncleaned XML column
myfile['Methods'] = ['' for x in range(len(myfile['Combo']))]
myfile.columns = ['Type','Scenario','Test','TestName','Combo','XML','Methods']
myfile['Methods'] = listofallfiles
myfile['Asserts'] = ['' for x in range(len(myfile['Combo']))]
myfile.columns = ['Type','Scenario','Test','TestName','Combo','XML','Methods', 'Asserts']
myfile['Asserts'] = listofallfiles
myfile['Methods_Asserts'] = ['' for x in range(len(myfile['Combo']))]
myfile.columns = ['Type','Scenario','Test','TestName','Combo','XML','Methods', 'Asserts','Methods_Asserts']
myfile['Methods_Asserts']=listofallfiles
myfile['Assert_Only'] = ['' for x in range(len(myfile['Combo']))]
myfile.columns = ['Type','Scenario','Test','TestName','Combo','XML','Methods', 'Asserts','Methods_Asserts','Assert_Only']
myfile['Assert_Only']=listofallfiles


new = []
for i in range(testlen):
    new.append(i)
myfile['Index'] = new
myfile.columns = ['Type','Scenario','Test','TestName','Combo','XML','Methods', 'Asserts','Methods_Asserts','Assert_Only','Index']


#isolating methods and assertions

counter = 0
for file in listofallfiles:
    stringstuff = ''
    assertstuff = ''
    expressionstuff = ''
    finalassertname = ''
    namestring = ''
    rootspot = ET.fromstring(file)
    findfunction = rootspot.find('function/block/block_content')
    tagstring = (ET.tostring(findfunction,encoding = 'unicode'))
    #print(tagstring)
    for element in findfunction:
        if (element.tag == 'decl_stmt'):
            for el in element:
                if el.tag == 'decl':
                    for item in el:
                        if item.tag == 'init':
                            for call in item:
                                if call.tag == 'expr':
                                    for name in item:
                                        if name.tag == 'expr':
                                            for item in name:
                                                for call in item:
                                                    if call.tag == 'name':
                                                        methods_notrycatch_noasserts = (ET.tostring(call,encoding = 'unicode'))
                                                        stringstuff+=methods_notrycatch_noasserts
                                                        expressionstuff +=methods_notrycatch_noasserts
        elif(element.tag=='try'):
            tagstring = (ET.tostring(element,encoding = 'unicode'))
            for item in element:
                if item.tag=='block':
                    for block in item:
                        if block.tag =='block_content':
                            for trystmt in block:
                                if trystmt.tag == 'expr_stmt':
                                    for element in trystmt:
                                        if element.tag=='expr':
                                            for expr in element:
                                                if expr.tag =='call':
                                                    for child in expr:
                                                        if child.tag == 'name':
                                                            trystuff = (ET.tostring(child,encoding = 'unicode'))
                                                            stringstuff += trystuff
                                                            expressionstuff += trystuff
        elif(element.tag == 'expr_stmt'):
            for element2 in element:
                if element2.tag == 'expr':
                    for expr in element2:
                        if expr.tag == 'call':
                            for call in element:
                                if call.tag == 'expr':
                                    for expr in call:
                                        if expr.tag =='call':
                                            for file in expr:
                                                if file.tag == 'name':
                                                    assertname = (ET.tostring(file,encoding = 'unicode'))
                                                    assertstuff += assertname
                                                    expressionstuff += assertname
                                                    finalassertname = assertname
                                                elif file.tag =='argument_list':
                                                    for element in file:
                                                        if element.tag == 'argument':
                                                            for item in element:
                                                                if item.tag == 'expr':
                                                                    for child in item:
                                                                        if child.tag == 'call':
                                                                            for children in child:
                                                                                if children.tag == 'name':
                                                                                    for name in children:
                                                                                        if name.tag =='name':
                                                                                            namespot = (ET.tostring(name,encoding = 'unicode'))
                                                                                            assertstuff += namespot
                                                                                            expressionstuff+=namespot

    myfile['Methods'][counter] = stringstuff
    myfile['Asserts'][counter] = assertstuff
    myfile['Methods_Asserts'][counter] = expressionstuff
    myfile['Assert_Only'][counter] = finalassertname
    counter += 1

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
