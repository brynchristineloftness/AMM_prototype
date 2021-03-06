from imports import *

def makepacksandprunes(myfile,testlen,scenariocorpus,defaultgrid,oracle,mpmoracle):
    prune1 = scenariomodel(myfile,testlen,scenariocorpus,defaultgrid,oracle,mpmoracle)
    prune3 = tfidf_model(myfile,testlen,.84,'bnn',defaultgrid,scenariocorpus,oracle,mpmoracle)
    prune4 = lsi_prune(myfile,defaultgrid,testlen,oracle,mpmoracle)
    prunepack = prune1 + prune3+prune4
    prunepack= sortstuff(prunepack)
    return prune1,prune3,prune4,prunepack

def sortstuff(name):
    name = sorted(name)
    for item in range(len(name)):
        name[item] = sorted(name[item],reverse=False)
    name = sorted(name)
    name_set = set(tuple(x) for x in name)
    name = [ list(x) for x in name_set ]
    return name


def longest_common_subsequence(myfile,testlen,num):
    #minimum length of tests compared less longest common subsequence with asserts, returns list of LCS valid tests
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

def intersect(name,myfile,intersectiongrid,testlen):
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
            intersectiongrid[test][test2] = metric
            if (test == test2):
                intersectiongrid[test][test2] = 0
            setcountertest2 = 0
            intersection = 0
        setcountertest = 0
    return intersectiongrid

def setmetrics_combo(myfile,testlen,defaultgrid,column,num,oracle,mpmoracle):
    intersectiongrid = defaultgrid     
    intersectiongrid = intersect(column,myfile,intersectiongrid,testlen)
    official_list = []
    listsorted = []
    official_list, listsorted = createsortedlist(intersectiongrid)
    listsorted = sorted(listsorted, key=lambda x: x[0])
    listsorted = list(set(tuple(x) for x in listsorted))
    official_list, listsorted = compute(official_list, listsorted,num)
    setintersectionresults, index_list_methods = printresults(official_list,'Full Results for Methods (no args or suite name)',myfile)
    setintersection_Combo_51_RESULTS = setintersectionresults #pack15
    return setintersection_Combo_51_RESULTS

def convertindextoname(index_list,myfile):
    for pair in range(len(index_list)):
        firstnumber = index_list[pair][0]
        secondnumber = index_list[pair][1]
        index_list[pair][0]= myfile['TestName'][firstnumber] 
        index_list[pair][1]= myfile['TestName'][secondnumber] 
    index_list = sortstuff(index_list)
    return index_list

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


def scenariomodel(myfile,testlen,scenariocorpus,defaultgrid,oracle,mpmoracle):
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
    skipgramresults, index_list = printresults(official_list_skipgram,'Full Results for Skipgram',myfile)
    index_list = convertindextoname(index_list,myfile)
    skipgram_scenario_PRUNE = index_list #len = 249
    return skipgram_scenario_PRUNE

def printresults(officiallist,stringstuff,myfile):
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


def tfidf_model(myfile,testlen,num,typetfidf,defaultgrid,scenariocorpus,oracle,mpmoracle):
    tfidfgrid = defaultgrid
    tfidfgrid = tfidfcorptogrid(scenariocorpus,testlen,tfidfgrid,typetfidf)
    official_list_tfidf, mainlistsorted = createsortedlist(tfidfgrid)
    mainlistsorted = sorted(mainlistsorted, key=lambda x: x[0])
    mainlistsorted = list(set(tuple(x) for x in mainlistsorted))
    official_list_tfidf, mainlistsorted = compute(official_list_tfidf, mainlistsorted,num)
    tfidfresults, index_list = printresults(official_list_tfidf,'Full Results for TFIDF',myfile)
    index_list = convertindextoname(index_list,myfile)
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


def lsi_prune(myfile,defaultgrid,testlen,oracle,mpmoracle):
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
    lsiresults, index_list = printresults(official_lsi_list,'Full Results for LSI',myfile)
    lsi_scenario_PRUNE = lsiresults
    return lsi_scenario_PRUNE