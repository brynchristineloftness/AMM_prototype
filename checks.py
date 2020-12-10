from imports import *


def defineAutoandManual(myfile):
    manuallist = []
    autolist = []
    for item in range(len(myfile['Type'])):
        if myfile['Type'][item] == "Manual":
            manuallist.append(myfile['TestName'][item])
        else:
            autolist.append(myfile['TestName'][item])
    return manuallist, autolist
    
def layer1(myfile,testlen,autolist,manuallist,oracle,mpmoracle):
    keep_pack = []
    group1 = longest_common_subsequence(myfile,testlen,4)
    group1real = []
    for item in group1:
        if item[0] in autolist and item[1] in manuallist:
            group1real.append(item)
    group1 = group1real

    print('layer1',len(group1),1)
    keep_pack += group1
    #returns list of pairs with assert common subsequences > 4 that are auto versus manual, accounting for assert lengths
    return group1,keep_pack

def layer2(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,oracle,mpmoracle,scenariocorpus):
    group2 = setmetrics_combo(myfile,testlen,defaultgrid,"Combo",.51,oracle,mpmoracle)
    group2 = sortstuff(group2)
    group2real = []
    for item in group2:
        if item[0] in autolist and item[1] in manuallist:
            group2real.append(item)
    group2 = group2real

    prune_scenario = setmetrics_combo(myfile,testlen,defaultgrid,"Scenario",.7889,oracle,mpmoracle)
    #branch decision tree
    group3 = [x for x in group2 if x in prune_scenario]
    group2 = [x for x in group2 if x not in prune_scenario]

    prune_asserts = setmetrics_combo(myfile,testlen,defaultgrid,"Asserts",.35,oracle,mpmoracle)
    group2 = [x for x in group2 if x not in prune_asserts]

    prune_asserts = setmetrics_combo(myfile,testlen,defaultgrid,"Methods_Asserts",.68,oracle,mpmoracle)
    
    #branch decision tree
    group4 = [x for x in group2 if x not in prune_asserts]
    group2 = [x for x in group2 if x in prune_asserts]

    split = tfidf_model(myfile,testlen,.65,'bnn',defaultgrid,scenariocorpus,oracle,mpmoracle)
    group2 = [x for x in group2 if x in split]

    print('layer2',len(group2),2) 
    keep_pack+=group2

    return group2,group3,group4,keep_pack

def layer3(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,group3,oracle,mpmoracle,scenariocorpus):
    group3 = sortstuff(group3)

    prune_asserts = setmetrics_combo(myfile,testlen,defaultgrid,"Methods_Asserts",.9999,oracle,mpmoracle)
    group3 = [x for x in group3 if x in prune_asserts]

    split = tfidf_model(myfile,testlen,.785,'bnn',defaultgrid,scenariocorpus,oracle,mpmoracle)
    group3 = [x for x in group3 if x in split]

    print('layer3',len(group3),2) 
    keep_pack+=group3
    return group3, keep_pack


def layer4(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,group4,oracle,mpmoracle,scenariocorpus):
    group4 = sortstuff(group4)

    add_methods = setmetrics_combo(myfile,testlen,defaultgrid,"Methods",.9995,oracle,mpmoracle)
    group5 = [x for x in group4 if x in add_methods]
    group4 = [x for x in group4 if x not in add_methods]
    prune_scenario = setmetrics_combo(myfile,testlen,defaultgrid,"Scenario",.7,oracle,mpmoracle)
    group4 = [x for x in group4 if x not in prune_scenario]

    split = tfidf_model(myfile,testlen,.605,'bnn',defaultgrid,scenariocorpus,oracle,mpmoracle)
    group4 = [x for x in group4 if x not in split]
    print('layer4',len(group4),2)
    keep_pack+=group4
    return group4, group5, keep_pack

def layer5(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,group5,oracle,mpmoracle,scenariocorpus):
    prune_scenario = setmetrics_combo(myfile,testlen,defaultgrid,"Scenario",.69,oracle,mpmoracle)
    group5 = [x for x in group5 if x not in prune_scenario]

    prune_scenario = setmetrics_combo(myfile,testlen,defaultgrid,"Combo",.59,oracle,mpmoracle)
    group5 = [x for x in group5 if x not in prune_scenario]


    split = tfidf_model(myfile,testlen,.58,'bnn',defaultgrid,scenariocorpus,oracle,mpmoracle)
    group5 = [x for x in group5 if x not in split]


    print('layer5',len(group5),3)
    keep_pack+=group5

    return group5, keep_pack

def checklayers(group1,group2,group3,group4,group5,oracle,mpmoracle,prunepack):
    group1count=0
    group2count=0
    group3count=0
    group4count=0
    group5count = 0
    for item in group4:
        if item in prunepack:
            group4 = [x for x in group4 if x != item]
    for item in group5:
        if item in prunepack:
            group5 = [x for x in group5 if x != item]
    for item in oracle:
        if item in group1:
            group1count+=1
        if item in group2 and item not in group1:
            group2count+=1
        if item in group3 and item not in group2 and item not in group1:
            group3count+=1
        if item in group4 and item not in group3 and item not in group2 and item not in group1:
            group4count+=1
        if item in group5 and item not in group4 and item not in group3 and item not in group2 and item not in group1:
            group5count+=1
    print("oracle:")
    print(len(group1),group1count)
    print(len(group2),group2count)
    print(len(group3),group3count)
    print(len(group4),group4count)
    print(len(group5),group5count)
    group1count=0
    group2count=0
    group3count=0
    group4count=0
    group5count = 0
    for item in mpmoracle:
        if item in group1:
            group1count+=1
        if item in group2 and item not in group1:
            group2count+=1
        if item in group3 and item not in group2 and item not in group1:
            group3count+=1
        if item in group4 and item not in group3 and item not in group2 and item not in group1:
            group4count+=1
        if item in group5 and item not in group4 and item not in group3 and item not in group2 and item not in group1:
            group5count+=1
    print("mpmoracle:")
    print(len(group1),group1count)
    print(len(group2),group2count)
    print(len(group3),group3count)
    print(len(group4),group4count)
    print(len(group5),group5count)


def defineTest(keep_pack,oracle,mpmoracle,manuallist,autolist,group1,group2,group3,group4,group5):
    epic1 = keep_pack
    counter = 0
    counter2 = 0
    epic1 = sortstuff(epic1)
    print()
    for item in sorted(epic1):
        if item in oracle :
            print('*o*',end='')
            counter+=1
        if item in mpmoracle:
            print("*mpm*",end = '')
            counter2+=1
        if item not in oracle and item not in mpmoracle:
            print("bad",end = '')
        print (item)
    print()
    print("found in oracle: ",counter,'out of',len(oracle))
    tp_oracle = counter
    print("found in mpm: ",counter2,'out of',len(mpmoracle))
    tp_mpmoracle = counter2
    print('num of matches given: ',len(epic1))
    total = len(epic1)
    fp_oracle = total - tp_oracle
    fp_mpmoracle = total - tp_mpmoracle
    numofautos = len(autolist)
    numofmanuals = len(manuallist)
    maxpossible = numofautos*numofmanuals
    print('total possible num of matches:', maxpossible)
    tn_oracle = maxpossible-fp_oracle
    tn_mpmoracle = maxpossible-fp_mpmoracle
    fn_oracle = len(oracle)-counter
    fn_mpmoracle = len(mpmoracle)-counter2
    accuracy_oracle = (tp_oracle + tn_oracle)/(tp_oracle + tn_oracle +fp_oracle+fn_oracle)
    accuracy_mpmoracle = (tp_mpmoracle+tn_mpmoracle)/(tp_mpmoracle + tn_mpmoracle +fp_mpmoracle+fn_mpmoracle)
    precision_oracle = (tp_oracle)/(tp_oracle+fp_oracle)
    precision_mpmoracle = (tp_mpmoracle)/(tp_mpmoracle+fp_mpmoracle)
    recall_oracle = (tp_oracle)/(tp_oracle+fn_oracle)
    recall_mpmoracle = (tp_mpmoracle)/(tp_mpmoracle+fn_mpmoracle)
    f1_oracle = 2*((precision_oracle*recall_oracle)/(precision_oracle+recall_oracle))
    f1_mpmoracle = 2*((precision_mpmoracle*recall_mpmoracle)/(precision_mpmoracle+recall_mpmoracle))
    print()
    print('STATS')
    print('-----------------------')
    print('accuracy for oracle:',accuracy_oracle)
    print('accuracy for mpmoracle:',accuracy_mpmoracle)
    print()
    print('precision for oracle:',precision_oracle)
    print('precision for mpmoracle:',precision_mpmoracle)
    print()
    print('recall for oracle:',recall_oracle)
    print('recall for mpmoracle:',recall_mpmoracle)
    print()
    print('f1 for oracle:',f1_oracle)
    print('f1 for mpmoracle:',f1_mpmoracle)
