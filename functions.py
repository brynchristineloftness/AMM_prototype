from imports import *

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


def showfigure(grid):
    figure = plt.pcolormesh(grid,vmax = 1.0,cmap=cmap,edgecolors='k', linewidths=.5)
    plt.colorbar(figure)
    plt.show(figure)
    


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
