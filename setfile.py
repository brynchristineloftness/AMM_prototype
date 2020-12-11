from imports import *



def defineoracles():
    optionbuilder_oracle = [['testCompleteOption','test02'],['testCompleteOption','test05'],['testCompleteOption','test08'],
        ['testCompleteOption','test19'],['testCompleteOption','test22'], ['testTwoCompleteOptions','test08'],
        ['testTwoCompleteOptions','test19'],['testTwoCompleteOptions','test22'], ['testBaseOptionCharOpt','test08'],
        ['testIllegalOptions', 'test14'],['testSpecialOptChars','test15'],['testCreateIncompleteOption','test16'],
        ['testOptionArgNumbers','test21']]

        #merges and partial merge oracle       
    optionbuilder_mpmoracle = [['testCompleteOption','test02'],['testCompleteOption','test05'],['testCompleteOption','test08'],
            ['testCompleteOption','test19'],['testCompleteOption','test22'], ['testTwoCompleteOptions','test08'],
            ['testTwoCompleteOptions','test19'],['testTwoCompleteOptions','test22'], ['testBaseOptionCharOpt','test08'],
            ['testIllegalOptions', 'test14'],['testSpecialOptChars','test15'],['testCreateIncompleteOption','test16'],
            ['testOptionArgNumbers','test21'], ['testCompleteOption','test06'], ['testCompleteOption','test28'], 
                ['testCompleteOption','test29'],['testTwoCompleteOptions','test28'],['testTwoCompleteOptions','test29']]          

    commandline_oracle = [['testGetOptions','test00'],['testBuilder','test01'],['testBuider','test08'],
    ['testBuilder','test09'],['testGetOptions','test10'],['testGetParsedOptionValue','test27'],
    ['testGetParsedOptionValue','test28'],['testGetParsedOptionValue','test29'],
    ['testGetOptionProperties','test33'],['testGetOptionProperties','test32'],
    ['testBuilder','test40']]

    commandline_mpmoracle = [['testGetParsedOptionValue','test26'],['testGetOptionProperties','test30'],
    ['testGetOptions','test00'],['testBuilder','test01'],['testBuider','test08'],
    ['testBuilder','test09'],['testGetOptions','test10'],['testGetParsedOptionValue','test27'],
    ['testGetParsedOptionValue','test28'],['testGetParsedOptionValue','test29'],
    ['testGetOptionProperties','test33'],['testGetOptionProperties','test32'],['testBuilder','test40']]
        
    util_oracle = [['testStripLeadingHyphens','test06'],['testStripLeadingHyphens','test07'],
    ['testStripLeadingHyphens','test08'],['testStripLeadingAndTrailingQuotes','test00'],
    ['testStripLeadingAndTrailingQuotes','test02'],['testStripLeadingAndTrailingQuotes','test03'],
    ['testStripLeadingAndTrailingQuotes','test04'],['testStripLeadingAndTrailingQuotes','test05']]

    util_mpmoracle = [['testStripLeadingHyphens','test06'],['testStripLeadingHyphens','test07'],
    ['testStripLeadingHyphens','test08'],['testStripLeadingAndTrailingQuotes','test00'],
    ['testStripLeadingAndTrailingQuotes','test02'],['testStripLeadingAndTrailingQuotes','test03'],
    ['testStripLeadingAndTrailingQuotes','test04'],['testStripLeadingAndTrailingQuotes','test05']]

    options_oracle = [[]]

    options_mpmoracle = [['testDuplicateSimple','test05'],['testLong','test18'],
    ['testLong','test19'],['testGetOptionsGroups','test28']]

    optiongroup_oracle = [[]]

    optiongroup_mpmoracle = [['testToString','test05'],['testToString','test06']]

    option_oracle = [['testBuilderMethods','test96']]

    option_mpmoracle = [['testBuilderMethods','test46'],['testBuilderMethods','test48'],
    ['testBuilderMethods','test49'],['testBuilderMethods','test50'],
    ['testBuilderMethods','test51'],['testBuilderMethods','test53'],
    ['testBuilderMethods','test55'],['testBuilderMethods','test56'],
    ['testClone','test57'],['testHasArgs','test65'],['testHasArgs','test70'],
    ['testHasArgs','test71'],['testHasArgs','test72'],['testHasArgs','test71'],
    ['testHasArgName','test72'],['testHasArgName','test73'],
    ['testBuilderMethods','test79'],['testHasArgs','test83'],['testBuilderMethods','test96']]

    helpformatter_oracle = [['testFindWrapPos','test07'],['testRtrim','test02'],
    ['testPrintOptions,test30'],[testRtrim,test47]]

    for item in optionbuilder_oracle:
        item = item.sort()

    for item in optionbuilder_mpmoracle:
        item = item.sort()

    return optionbuilder_oracle, optionbuilder_mpmoracle

def setparsefile():
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
    return autotree, autoroot, manualtree, manualroot,cleanautotree,cleanautoroot,cleanmanualtree,cleanmanualroot


def definefile():
    myfile = pd.read_csv(r"OptionBuilder.csv",header = 0)
    return myfile