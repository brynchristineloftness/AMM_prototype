from imports import *

def main():
    oracle, mpmoracle = defineoracles()
    myfile = definefile()
    oraclecluster, mpmoraclecluster = cleanoracles(oracle,mpmoracle)
    myfile,mybackupfile = cleanfile(myfile)
    myfile,scenariocorpus,testcorpus,combinedcorpus,testlen = preprocess(myfile)
    defaultgrid = [[0 for i in range(testlen)] for j in range(testlen)]
    autotree, autoroot, manualtree, manualroot,cleanautotree,cleanautoroot,cleanmanualtree,cleanmanualroot = setparsefile()
    cleanautoroot,cleanmanualroot = cleanparsefiles(cleanautoroot,cleanmanualroot)
    myfile,listofallfiles = addxmltofile(myfile,cleanmanualroot,cleanautoroot,testlen)
    myfile = isolatemethods_asserts(myfile,listofallfiles)
    myfile = cleancolumns(myfile)
    prune1,prune3,prune4,prunepack= makepacksandprunes(myfile,testlen,scenariocorpus,defaultgrid,oracle,mpmoracle)
    manuallist,autolist = defineAutoandManual(myfile)
    group1,keep_pack = layer1(myfile,testlen,autolist,manuallist,oracle,mpmoracle)
    group2,group3,group4, keep_pack = layer2(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,oracle,mpmoracle,scenariocorpus)
    group3, keep_pack = layer3(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,group3,oracle,mpmoracle,scenariocorpus)
    group4, group5, keep_pack = layer4(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,group4,oracle,mpmoracle,scenariocorpus)
    group5, keep_pack = layer5(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,group5,oracle,mpmoracle,scenariocorpus)
    checklayers(group1,group2,group3,group4,group5,oracle,mpmoracle,prunepack)
    keep_pack = [x for x in keep_pack if x not in prunepack]
    defineTest(keep_pack,oracle,mpmoracle,manuallist,autolist,group1,group2,group3,group4,group5)

main()


