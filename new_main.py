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
    pack3, prune1,prune3,prune4,prunepack= makepacksandprunes(myfile,testlen,scenariocorpus,defaultgrid,oracle,mpmoracle)
    manuallist,autolist = defineAutoandManual(myfile)
    round1,keep_pack = round1func(myfile,testlen,autolist,manuallist,oracle,mpmoracle)
    round2,round3,round4, keep_pack = round2func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,oracle,mpmoracle,scenariocorpus,prunepack)
    round3, keep_pack = round3func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,round3,oracle,mpmoracle,prunepack,scenariocorpus)
    round4, round5, keep_pack = round4func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,round4,oracle,mpmoracle,prunepack,scenariocorpus)
    round5, keep_pack = round5func(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,round5,oracle,mpmoracle,prunepack,scenariocorpus)
    defineTest(keep_pack,oracle,mpmoracle)

main()


