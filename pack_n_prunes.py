from imports import *

def makepacksandprunes(myfile,testlen):
    
    pack3 = one_2_one_asserts(myfile,testlen)
    prune1 = scenariomodel(myfile,testlen)
    prune3 = tfidf_model(myfile,testlen,.84,'bnn')
    prune4 = lsi_prune(myfile)
    prunepack = prune1 + prune3+prune4
    prunepack= sortstuff(prunepack)
    return pack3, prune1,prune3,prune4,prunepack

def sortstuff(name):
    name = sorted(name)
    for item in range(len(name)):
        name[item] = sorted(name[item])
    name = sorted(name)
    name_set = set(tuple(x) for x in name)
    name = [ list(x) for x in name_set ]
    return name

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


def computelower(officiallist, sortedlist, breakpoint):
    valuelist = []
    for group in sortedlist:
        if(group[2] < breakpoint):
            if (group[0]!=officiallist[-1][1] and group[1] != officiallist[-1][0]):
                officiallist.append(group)
    officiallist.remove(officiallist[0])
    return officiallist,sortedlist


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

def compute(officiallist, sortedlist, breakpoint):
    valuelist = []
    for group in sortedlist:
        if(group[2] > breakpoint):
            if (group[0]!=officiallist[-1][1] and group[1] != officiallist[-1][0]):
                officiallist.append(group)
    officiallist.remove(officiallist[0])
    return officiallist,sortedlist


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