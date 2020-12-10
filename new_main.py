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
    round1,keep_pack = layer1(myfile,testlen,autolist,manuallist,oracle,mpmoracle)
    round2,round3,round4, keep_pack = layer2(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,oracle,mpmoracle,scenariocorpus)
    round3, keep_pack = layer3(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,round3,oracle,mpmoracle,scenariocorpus)
    round4, round5, keep_pack = layer4(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,round4,oracle,mpmoracle,scenariocorpus)
    round5, keep_pack = layer5(myfile,testlen,defaultgrid,autolist,manuallist,keep_pack,round5,oracle,mpmoracle,scenariocorpus)
    keep_pack = [x for x in keep_pack if x not in prunepack]
    defineTest(keep_pack,oracle,mpmoracle,manuallist,autolist)

main()


