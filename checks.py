#round3 = round1, round4 = round2, round1 = round3,round6 = round4, round7 = round5, round8 = round6


def defineAutoandManual(myfile):
    manuallist = []
    autolist = []
    for item in range(len(myfile['Type'])):
        if myfile['Type'][item] == "Manual":
            manuallist.append(myfile['TestName'][item])
        else:
            autolist.append(myfile['TestName'][item])
    return manuallist, autolist
    
def round1func(myfile,testlen,autolist,manuallist):
    keep_pack = []
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

    return round3,keep_pack

def round2func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack):
    round4 = setmetrics_combo(myfile,testlen,defaultgrid,"Combo",.51)
    round4 = sortstuff(round4)
    round4real = []
    for item in round4:
        if item[0] in autolist and item[1] in manuallist:
            round4real.append(item)
    round4 = round4real

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

    return round4,round1,round6,keep_pack

def round3func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,round1):
    round1 = sortstuff(round1)
    round1 = [x for x in round1 if x not in prunepack]

    prune_asserts = setmetrics_combo(myfile,testlen,defaultgrid,"Methods_Asserts",.9999)
    round1 = [x for x in round1 if x in prune_asserts]

    split = tfidf_model(myfile,testlen,.785,'bnn')
    round1 = [x for x in round1 if x in split]

    print('one',len(round1),2) 
    prototypecheck(round1)
    keep_pack+=round1
    return round1, keep_pack


def round4func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,round6):
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
    return round6, round7, keep_pack

def round5func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,round7):
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

    return round7, keep_pack

def round6func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack):
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

    return round8,keep_pack


def defineTest(keep_pack,oracle,mpmoracle):
    epic1 = keep_pack
    counter = 0
    counter2 = 0
    for item in sorted(epic1):
        if item in oracle :
            print('*o*',end='')
            counter+=1
        if item in mpmoracle:
            print("*mpm*",end = '')
            counter2+=1
        print (item)
    print("found in oracle: ",counter,'out of',len(oracle))
    print("found in mpm: ",counter2,'out of',len(mpmoracle))
    print('number of matches',len(epic1))
