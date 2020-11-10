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
            intersectiongrid[test][test2] = metric
            if (test == test2):
                intersectiongrid[test][test2] = 0
            setcountertest2 = 0
            intersection = 0
        setcountertest = 0
    return intersectiongrid