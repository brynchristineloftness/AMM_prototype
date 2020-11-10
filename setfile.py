def defineoracles():
    oracle = [['testCompleteOption','test02'],['testCompleteOption','test05'],['testCompleteOption','test08'],
        ['testCompleteOption','test19'],['testCompleteOption','test22'], ['testTwoCompleteOptions','test08'],
        ['testTwoCompleteOptions','test19'],['testTwoCompleteOptions','test22'], ['testBaseOptionCharOpt','test08'],
        ['testIllegalOptions', 'test14'],['testSpecialOptChars','test15'],['testCreateIncompleteOption','test16'],
        ['testOptionArgNumbers','test21']]
        
    #merges and partial merge oracle       
    mpmoracle = [['testCompleteOption','test02'],['testCompleteOption','test05'],['testCompleteOption','test08'],
            ['testCompleteOption','test19'],['testCompleteOption','test22'], ['testTwoCompleteOptions','test08'],
            ['testTwoCompleteOptions','test19'],['testTwoCompleteOptions','test22'], ['testBaseOptionCharOpt','test08'],
            ['testIllegalOptions', 'test14'],['testSpecialOptChars','test15'],['testCreateIncompleteOption','test16'],
            ['testOptionArgNumbers','test21'], ['testCompleteOption','test06'], ['testCompleteOption','test28'], 
                ['testCompleteOption','test29'],['testTwoCompleteOptions','test28'],['testTwoCompleteOptions','test29']]          
    
    return oracle, mpmoracle

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