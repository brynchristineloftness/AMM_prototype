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

myfile = pd.read_csv(
    r"OptionBuilder.csv",header = 0)

def lsi_prune(myfile):
    entries = myfile['Scenario'].tolist()
    entries = [[ele for ele in sub if not ele.isdigit()] for sub in entries] 
    dict_for_lsi = Dictionary(entries)
    corp = [dict_for_lsi.doc2bow(line) for line in entries]
    lsi = models.LsiModel(corp,num_topics = 3)
    corp_lsi = lsi[corp]
    #transforms corpus to lsi space and indexes it
    index_lsi = similarities.MatrixSimilarity(corp_lsi) 
    sims= index_lsi[corp_lsi]
    lsi_grid = defaultgrid
    for i,s in enumerate(sims):
        for counter in range(testlen):
            lsi_grid[i][counter] = s[counter]
            if (i == counter):
                lsi_grid[i][counter] = 0
    official_lsi_list, lsi_listsorted = createsortedlist(lsi_grid)
    listsorted = sorted(lsi_listsorted, key=lambda x: x[0])
    listsorted = list(set(tuple(x) for x in listsorted))
    official_lsi_list, lsi_listsorted = computelower(official_lsi_list, lsi_listsorted,.69)
    lsiresults, index_list = printresults(official_lsi_list,'Full Results for LSI')
    results = TPFPoutput(lsiresults,oracle,mpmoracle)
    lsi_scenario_PRUNE = lsiresults
    return lsi_scenario_PRUNE

def setmetrics_combo(myfile,testlen,defaultgrid,column,num):
    intersectiongrid = defaultgrid     
    intersectiongrid = intersect(column,myfile,intersectiongrid)
    official_list = []
    listsorted = []
    official_list, listsorted = createsortedlist(intersectiongrid)
    listsorted = sorted(listsorted, key=lambda x: x[0])
    listsorted = list(set(tuple(x) for x in listsorted))
    official_list, listsorted = compute(official_list, listsorted,num)
    setintersectionresults, index_list_methods = printresults(official_list,'Full Results for Methods (no args or suite name)')
    results = TPFPoutput(setintersectionresults,oracle,mpmoracle)
    setintersection_Combo_51_RESULTS = setintersectionresults #pack15
    return setintersection_Combo_51_RESULTS

def intersectasserts_withassertadditive(myfile,testlen):
    assertgrid = defaultgrid
    assertgrid = intersectwithasserts('Asserts',assertgrid)
    officiallist, listsorted = createsortedlist(assertgrid)
    for item in listsorted:
        if [item[1],item[0],item[2]] in listsorted:
            listsorted.remove(item)

    listsorted = sorted(listsorted, key=lambda x: x[0])
    listsorted = list(set(tuple(x) for x in listsorted))

    officiallist, listsorted = compute(officiallist, listsorted, 1.74)
    setintersectionresults, index_list = printresults(officiallist,'Full Results for Asserts')
    results = TPFPoutput(setintersectionresults,oracle,mpmoracle)
    intersect_withassertadditive_99_RESULTS =setintersectionresults #pack21 
    return intersect_withassertadditive_99_RESULTS

def scenariomodel(myfile,testlen):
    scenariomodel_skipgram = Word2Vec(scenariocorpus,window=5,min_count=1,iter = 15,alpha=.2,sg=1,size = 75,seed = 0)
    scenariomodelskipgram_grid = defaultgrid

    #finding similarity for all manual against all auto, placed results in grid
    for test in range(testlen):
        for test2 in range(testlen):
            num = scenariomodel_skipgram.wv.n_similarity(myfile['Scenario'][test],myfile['Scenario'][test2])
            scenariomodelskipgram_grid[test][test2] = num
    #finding minimum similarity value
    minimum = 1.0
    for i,row in enumerate(scenariomodelskipgram_grid):
        for j, cell in enumerate(row):
            if (cell < minimum):
                minimum = scenariomodelskipgram_grid[i][j] 
    official_list_skipgram, mainlistsorted = createsortedlist(scenariomodelskipgram_grid)
    mainlistsorted = sorted(mainlistsorted, key=lambda x: x[0])
    mainlistsorted = list(set(tuple(x) for x in mainlistsorted))
    official_list_skipgram, mainlistsorted = computelower(official_list_skipgram, mainlistsorted,.86)
    skipgramresults, index_list = printresults(official_list_skipgram,'Full Results for Skipgram')
    results = TPFPoutput(skipgramresults,oracle,mpmoracle)
    index_list = convertindextoname(index_list)
    skipgram_scenario_PRUNE = index_list #len = 249
    return skipgram_scenario_PRUNE

def tfidf_model(myfile,testlen,num,typetfidf):
    tfidfgrid = defaultgrid
    tfidfgrid = tfidfcorptogrid(scenariocorpus,testlen,tfidfgrid,typetfidf)
    official_list_tfidf, mainlistsorted = createsortedlist(tfidfgrid)
    mainlistsorted = sorted(mainlistsorted, key=lambda x: x[0])
    mainlistsorted = list(set(tuple(x) for x in mainlistsorted))
    official_list_tfidf, mainlistsorted = compute(official_list_tfidf, mainlistsorted,num)
    tfidfresults, index_list = printresults(official_list_tfidf,'Full Results for TFIDF')
    results = TPFPoutput(tfidfresults,oracle,mpmoracle)
    index_list = convertindextoname(index_list)
    tfidf_bnn_scenario_RESULTS = index_list 
    return tfidf_bnn_scenario_RESULTS


def one_2_one_asserts(myfile,testlen):
    testlist_set = myfile['Asserts']

    matchlist = []
    for test in range(testlen):
        for test2 in range(testlen):
            if test !=test2:
                testone = testlist_set[test]
                testtwo = testlist_set[test2]
                if testone == testtwo and testone == []:
                    matchlist.append([myfile['TestName'][test],myfile['TestName'][test2]])
    matchlist = sortstuff(matchlist)
    one2one_asserts_RESULTS = matchlist #pack3
    return one2one_asserts_RESULTS

def longest_common_subsequence(myfile,testlen,num):
    testlist_set = myfile['Asserts']
    sublist = []
    sublist2 = []
    for test in range(testlen):
        for test2 in range(testlen):
            if test !=test2:
                testone = testlist_set[test]
                testtwo = testlist_set[test2]
                subsequencelen = lcs(testone,testtwo)
                minimum = min(len(testone),len(testtwo))
                subsequencelen = lcs(testone,testtwo)
                min_minus_lcs = minimum-subsequencelen
                if subsequencelen>num:
                    sublist.append([myfile['TestName'][test],myfile['TestName'][test2]])
    sublist = sortstuff(sublist)
    LCS_asserts_high = sublist
    return LCS_asserts_high


def sortstuff(name):
    name = sorted(name)
    for item in range(len(name)):
        name[item] = sorted(name[item])
    name = sorted(name)
    name_set = set(tuple(x) for x in name)
    name = [ list(x) for x in name_set ]
    return name

def intersectwithasserts(name,intersectiongrid):
    setcountertest = 0
    setcountertest2 = 0
    for test in range(testlen):
        for item in set((myfile[name][test])):
                setcountertest += 1
        for test2 in range(testlen):
            for item in set((myfile[name][test2])):
                setcountertest2 += 1
            intersection = set((myfile[name][test])).intersection(set((myfile[name][test2])))
            intersection = len(intersection)
            minimum = min(setcountertest,setcountertest2)
            if minimum != 0:
                metric = intersection/minimum
            else:
                metric = 0
            if 'assertNotNull' in myfile[name][test] and 'assertEquals' in myfile[name][test2]:
                metric += 1
            #print(setcountertest,setcountertest2,test,test2,intersection,metric)
            intersectiongrid[test][test2] = metric
            if (test == test2):
                intersectiongrid[test][test2] = 0
            setcountertest2 = 0
            intersection = 0
        setcountertest = 0
    return intersectiongrid

def prototypecheck(pack1):
    pack1 = sortstuff(pack1)
    counter = 0
    counter2 = 0
    itemlist = []
    for item in pack1:  
        if item in oracle:
            itemlist.append(item)
            counter +=1
        else: 
            counter2+=1
    print("Number of found combos", counter)
    print('printing items found in matchlist that are in oracle:')
    for item in sorted(itemlist):
        print(item) 
    print()
    question1 = sorted(pack1)[0][0]
    questionnum =1
    for item in sorted(pack1):
        print(item)
        if question1 != item[0]:
            question1 = item[0]
            questionnum+=1
    print('number of questions', questionnum)

def camel_case_split(str):
    words = [[str[0]]] 
    for c in str[1:]: 
        if words[-1][-1].islower() and c.isupper(): 
            words.append(list(c)) 
        else: 
            words[-1].append(c) 
    return [''.join(word) for word in words]

def tfidfcorptogrid(entries,testlen,tfidfgrid,IR):
    entries = [[ele for ele in sub if not ele.isdigit()] for sub in entries] 
    dict_for_tfidf = Dictionary(entries)
    corp = [dict_for_tfidf.doc2bow(line) for line in entries]
    tfidfmodel = TfidfModel(corp,smartirs = IR)   
    corp_tfidf = tfidfmodel[corp]
    index_tfidf = similarities.MatrixSimilarity(corp_tfidf)
    sims= index_tfidf[corp_tfidf]
    for i,s in enumerate(sims):
        for counter in range(testlen):
            tfidfgrid[i][counter] = s[counter]
            if (i == counter):
                tfidfgrid[i][counter] = 0
    return tfidfgrid

def lcs(X, Y): 
    m = len(X) 
    n = len(Y) 
    L = [[None]*(n + 1) for i in range(m + 1)] 
    for i in range(m + 1): 
        for j in range(n + 1): 
            if i == 0 or j == 0 : 
                L[i][j] = 0
            elif X[i-1] == Y[j-1]: 
                L[i][j] = L[i-1][j-1]+1
            else: 
                L[i][j] = max(L[i-1][j], L[i][j-1]) 
    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1] 
    return L[m][n] 

def compute(officiallist, sortedlist, breakpoint):
    valuelist = []
    for group in sortedlist:
        if(group[2] > breakpoint):
            if (group[0]!=officiallist[-1][1] and group[1] != officiallist[-1][0]):
                officiallist.append(group)
    officiallist.remove(officiallist[0])
    return officiallist,sortedlist

def prune(index_list,keeplist):
    x = 0
    for pair in index_list:
        if pair in keeplist:
            x+=1
            keeplist.remove(pair)
    print('Count of Pruned:',x)
    return keeplist

def convertindextoname(index_list):
    for pair in range(len(index_list)):
        firstnumber = index_list[pair][0]
        secondnumber = index_list[pair][1]
        index_list[pair][0]= myfile['TestName'][firstnumber] 
        index_list[pair][1]= myfile['TestName'][secondnumber] 
    index_list = sortstuff(index_list)
    return index_list

def convertnametoindex(name_list):
    for pair in range(len(name_list)):
        firstname = name_list[pair][0]
        secondname = name_list[pair][1]
        itemcount = 0
        itemcount2 = 0
        for item in myfile['TestName']:
            if item == firstname:
                name_list[pair][0] = itemcount
            elif item == secondname:
                name_list[pair][1] = itemcount2
            itemcount+=1
            itemcount2+=1
        itemcount = 0
        itemcount2 = 0
    return name_list

def computelower(officiallist, sortedlist, breakpoint):
    valuelist = []
    for group in sortedlist:
        if(group[2] < breakpoint):
            if (group[0]!=officiallist[-1][1] and group[1] != officiallist[-1][0]):
                officiallist.append(group)
    officiallist.remove(officiallist[0])
    return officiallist,sortedlist

def showfigure(grid):
    figure = plt.pcolormesh(grid,vmax = 1.0,cmap=cmap,edgecolors='k', linewidths=.5)
    plt.colorbar(figure)
    plt.show(figure)
    
def printresults(officiallist,stringstuff):
    full_list = []
    index_list = []
    info = ''   
    for thing in officiallist:
        info = [myfile['TestName'][thing[0]], myfile['TestName'][thing[1]]]
        indexinfo = [thing[0], thing[1]]
        index_list.append(indexinfo)
        full_list.append(info)
    results = sortstuff(full_list)
    index_list = sortstuff(index_list)
    return results, index_list


def check(oracle, official,name):
    print('checking:', name)
    counter = 0
    for group in official:
        counter +=1
        oraclereplica = [myfile['TestName'][group[0]],myfile['TestName'][group[1]]]
        if oraclereplica in oracle:
            print(oraclereplica,group[2],counter)
    print()
    for group in official:
        counter +=1
        oraclereplica = [myfile['TestName'][group[0]],myfile['TestName'][group[1]]]
        if item in oracle:
            print(oraclereplica,group[2])

def output(full_list,oracle,mpmoracle,truepositivelist,falsepositivelist,truepositivelistmpm,falsepositivelistmpm,testcluster,truepositive,falsepositive,tporacle,fporacle):
    print(len(testcluster),testlen)
    print('total in MPMoracle;',len(mpmoracle),'total predictions',len(full_list))
    print('true pos:',truepositive, '  ', 'false pos', falsepositive)
    if len(full_list) !=0:
        tprate = truepositive/len(full_list)
        fprate = falsepositive/len(full_list)
    else :
        tprate = 0
        fprate = 0
    #print("-----------")
    print('total in oracle',len(oracle),'total predictions',len(full_list))
    print('true pos:',tporacle, '  ', 'false pos', fporacle)
    if len(full_list) !=0:
        tprate_o = tporacle/len(full_list)
        fprate_o = fporacle/len(full_list)
    else :
        tprate_o = 0
        fprate_o = 0
    print('-----------')
    print('ORACLE:')
    print('tp rate:', tprate_o, '  ', 'fp rate:', fprate_o)
    #print(tprate_o, ',', fprate_o,',', tprate, ',',fprate)
    print('MPM ORACLE:')
    print('tp rate:', tprate, '  ', 'fp rate:', fprate)
    full_output_of_lists(full_list,oracle,mpmoracle,truepositivelist,falsepositivelist,truepositivelistmpm,falsepositivelistmpm,testcluster,truepositive,falsepositive,tporacle,fporacle)

def full_output_of_lists(full_list,oracle,mpmoracle,truepositivelist,falsepositivelist,truepositivelistmpm,falsepositivelistmpm,testcluster,truepositive,falsepositive,tporacle,fporacle):
    print('true positive list:')
    for file in truepositivelist:
        print(file)
    print()
    print("List of missed positives(false negatives) for merge-only oracle")
    for file in oracle:
        if file not in truepositivelist:
            print(file)
    print()   
    print("List of true positives for merge-only oracle")
    for file in oracle:
        if file in truepositivelist:
            print(file)
    print()        
    print("List of false positives for merge-only oracle")
    for file in falsepositivelist:
        print(file)
    print()        
    print("List of missed positives(false negatives) for merge/partial-merge oracle")
    for file in mpmoracle:
        if file not in truepositivelistmpm:
            print(file)
    print()
    print("List of true positives for merge/partial-merge oracle")
    for file in mpmoracle:
        if file in truepositivelistmpm:
            print(file) 
    print()
    print("List of false positives for merge/partial-merge oracle")
    for file in falsepositivelistmpm:
        print(file)
    

def TPFPoutput(full_list,oracle,mpmoracle):
    testcluster = []
    full_list = sorted(full_list)
    fl_set = set(tuple(x) for x in full_list)
    full_list = [ list(x) for x in fl_set ]
    for item in full_list:
        item = sorted(item)
    truepositive = 0
    falsepositive = 0
    tporacle = 0
    fporacle = 0
    truepositivelist = []
    falsepositivelist= []
    truepositivelistmpm= []
    falsepositivelistmpm = []
    for file in full_list:
        testcluster.append(file[0])
        testcluster.append(file[1])
        if file in mpmoracle:
            truepositive+=1
            truepositivelistmpm.append(file)
        else:
            falsepositive+=1
            falsepositivelistmpm.append(file)
        if file in oracle:
            tporacle += 1
            truepositivelist.append(file)
        else:
            fporacle +=1   
            falsepositivelist.append(file)
    testcluster = list(dict.fromkeys(testcluster))
    
    truepositivelist = sortstuff(truepositivelist)
    falsepositivelist = sortstuff(falsepositivelist)
    truepositivelistmpm = sortstuff(truepositivelistmpm)
    falsepositivelistmpm = sortstuff(falsepositivelistmpm)
    
    #output(full_list,oracle,mpmoracle,truepositivelist,falsepositivelist,truepositivelistmpm,falsepositivelistmpm,testcluster,truepositive,falsepositive,tporacle,fporacle)
    return full_list

def createsortedlist(grid):
    main_list = []
    counter = 0
    official_list = []
    stuff = ['','','']
    official_list.append(stuff)
    for i,row in enumerate(grid):
        for j, cell in enumerate(row):
            if (i!=j):
                stuff = [i, j, grid[i][j]]
                main_list.append(stuff)
    mainlistsorted = sortstuff(main_list)
    mainlistsorted = sorted(main_list, key=lambda x: x[-1], reverse=True)
    return official_list, mainlistsorted

def clean(column):
    myfile[column] = [entry.replace('/','') for entry in myfile[column]]      
    myfile[column] = [entry.replace('<call>',' ') for entry in myfile[column]]
    myfile[column] = [entry.replace('<operator>',' ') for entry in myfile[column]]
    myfile[column] = [entry.replace('<name>',' ') for entry in myfile[column]]
    myfile[column] = [entry.replace('<argument>',' ') for entry in myfile[column]]
    myfile[column] = [entry.replace('<list>',' ') for entry in myfile[column]]
    myfile[column] = [entry.replace('<argument_list>',' ') for entry in myfile[column]]
    myfile[column] = [entry.replace('<expr>',' ') for entry in myfile[column]]
    myfile[column] = [entry.replace('<literal>',' ') for entry in myfile[column]]
    myfile[column] = [entry.replace('<char>',' ') for entry in myfile[column]]
    myfile[column] = [entry.replace('<type>',' ') for entry in myfile[column]]
    myfile[column] = myfile[column].apply(lambda x:''.join([i for i in x if i not in string.punctuation]))
    
def intersect(name,myfile,intersectiongrid):
    setcountertest = 0
    setcountertest2 = 0
    for test in range(testlen):
        for item in set((myfile[name][test])):
                setcountertest += 1
        for test2 in range(testlen):
            for item in set((myfile[name][test2])):
                setcountertest2 += 1
            intersection = set((myfile[name][test])).intersection(set((myfile[name][test2])))
            intersection = len(intersection)
            minimum = min(setcountertest,setcountertest2)
            if minimum != 0:
                metric = intersection/minimum
            else:
                metric = 0
            #print(setcountertest,setcountertest2,test,test2,intersection,metric)
            intersectiongrid[test][test2] = metric
            if (test == test2):
                intersectiongrid[test][test2] = 0
            setcountertest2 = 0
            intersection = 0
        setcountertest = 0
    return intersectiongrid

#creating oracle
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
pack9 = longest_common_subsequence(myfile,testlen,4)
pack15 = setmetrics_combo(myfile,testlen,defaultgrid,"Combo",.51)
prune1 = scenariomodel(myfile,testlen)
pack24 = tfidf_model(myfile,testlen,.88,'bnn')
prune4 = lsi_prune(myfile)

manuallist = []
autolist = []

for item in range(len(myfile['Type'])):
    if myfile['Type'][item] == "Manual":
        manuallist.append(myfile['TestName'][item])
    else:
        autolist.append(myfile['TestName'][item])


deletepack = []

#round1 = 24
round1 = []
round1 = pack24
round1 = sortstuff(round1)
for item in round1:
    if item[0] in manuallist and item[1] in autolist:
        round1.remove(item)
    elif item[0] in autolist and item[1] in manuallist:
        round1.remove(item)
    elif item[0] in manuallist and item[1] in manuallist:
        round1.remove(item)


deletepack+= round1
prunepack = []
prunepack = setmetrics_combo(myfile,testlen,defaultgrid,"Methods",.98)
round1 = [x for x in round1 if x in prunepack]
prunepack = []
prunepack = setmetrics_combo(myfile,testlen,defaultgrid,"Test",.71)
round1 = [x for x in round1 if x in prunepack]

round1 = [x for x in round1 if x not in prune1]
round1 = [x for x in round1 if x not in prune4]
print('round1',len(round1), 3)
#---------------------------------

#round2 = 3
round2 = []
round2 = pack3
round2 = [x for x in round2 if x not in deletepack]

round2 = sortstuff(round2)
for item in round2:
    if item[0] in manuallist and item[1] in manuallist:
        round2.remove(item)
    elif item[0] in autolist and item[1] in autolist:
        round2.remove(item)
    elif item[0] in manuallist and item[1] in autolist:
        round2.remove(item)

deletepack +=round2

round2 = [x for x in round2 if x not in prune1]
round2 = [x for x in round2 if x not in prune4]
print('round2',len(round2),2) #2/8
#--------------------------------


round3 = []
round3 = (pack9)
round3 = [x for x in round3 if x not in deletepack]

round3 = sortstuff(round3)
for item in round3:
    if item[0] in manuallist and item[1] in autolist:
        round3.remove(item)
    elif item[0] in autolist and item[1] in autolist:
        round3.remove(item)

deletepack +=round3
prune = setmetrics_combo(myfile,testlen,defaultgrid,"Methods_Asserts",.75)
round3 = [x for x in round3 if x in prune]



round3 = [x for x in round3 if x not in prune1]
round3 = [x for x in round3 if x not in prune4]


print('round3',len(round3),4)
#-------
round4 = []
round4 = pack15
round4 = sortstuff(round4)
round4real = []
for item in round4:
    if item[0] in manuallist and item[1] in autolist:
        round4.remove(item)
    elif item[0] in autolist and item[1] in manuallist:
        round4real.append(item)
round4 = round4real


prune_scenario = setmetrics_combo(myfile,testlen,defaultgrid,"Scenario",.7889)
round4 = [x for x in round4 if x not in prune_scenario]

prune_asserts = setmetrics_combo(myfile,testlen,defaultgrid,"Asserts",.4)
round4 = [x for x in round4 if x not in prune_asserts]

round4 = [x for x in round4 if x not in deletepack]
deletepack+=round4
round4 = [x for x in round4 if x not in prune1]
round4 = [x for x in round4 if x not in prune4]

print('round4',len(round4),8) #3/60
#prototypecheck(round4)

#-------------------
round5 = []
round5 = tfidf_model(myfile,testlen,.52,'nfc')
round5 = sortstuff(round5)
round5 = [x for x in round5 if x not in deletepack]

round5real = []
for item in round5:
    if item[0] in autolist and item[1] in manuallist:
        round5real.append(item)
round5 = round5real

round5 = [x for x in round5 if x not in prune1]
round5 = [x for x in round5 if x not in prune4]
print('round5',len(round5),1) #3/60
#=========================

epic1 =  round1+round2+ round3+ round4+round5

epic1 = [x for x in epic1 if x not in prune1]
epic1 = [x for x in epic1 if x not in prune4]
epic1 = sortstuff(epic1)

print(len(epic1))
prototypecheck(epic1)
