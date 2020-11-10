from imports import *

def cleanoracles(oracle, mpmoracle):
    #sort and get rid of duplicates
    oracle = sortstuff(oracle)
    mpmoracle = sortstuff(mpmoracle)

    oraclecluster = []        
    for file in oracle:
            oraclecluster.append(file[0])
            oraclecluster.append(file[1])
    oraclecluster = list(dict.fromkeys(oraclecluster))

    mpmoraclecluster = []        
    for file in mpmoracle:
            mpmoraclecluster.append(file[0])
            mpmoraclecluster.append(file[1])
    mpmoraclecluster = list(dict.fromkeys(mpmoraclecluster))

    return oraclecluster, mpmoraclecluster

def cleanfile(myfile):
    #gets rid of new lines in strings for whole file
    myfile = myfile.replace(r'\n',' ', regex=True) 

    #gets rid of punct in scenarios
    myfile['Scenario'] = myfile['Scenario'].apply(
        lambda x:''.join([i for i in x if i not in string.punctuation])) 

    #gets rid of punct in tests and replaces with space
    myfile['Test'] = myfile['Test'].apply(lambda x:''.join([i for i in x if i not in string.punctuation]))

    #isolating test names and putting into column
    x = []
    testlist = myfile['Test'].tolist()
    x = re.compile('test')
    listofnames = []

    #define test name list
    for item in testlist: 
        txt = str(item)
        x = re.findall(r"\btest\w+", txt)
        listofnames.append(x)

    myfile['TestName'] = listofnames

    #gets rid of punctuation in Test Name Column
    myfile['TestName'] = myfile['TestName'].apply(lambda x:''.join([i for i in x if i not in string.punctuation])) 

    #separating camelcasing in scenarios and tests

    myfile['Scenario'] = myfile['Scenario'].apply(lambda x:[i for i in camel_case_split(x)])
    myfile['Scenario'] = myfile['Scenario'].apply(lambda x:' '.join([i for i in x]))
    myfile['Test'] = myfile['Test'].apply(lambda x:[i for i in camel_case_split(x)])
    myfile['Test'] = myfile['Test'].apply(lambda x:' '.join([i for i in x]))

    #makes all lowercase
    myfile['Test'] = myfile['Test'].apply(lambda x:''.join([i for i in x.lower()])) 
    myfile['Scenario'] = myfile['Scenario'].apply(lambda x:''.join([i for i in x.lower()])) 

    #creating new column with combined scenario and test words

    myfile['Combo'] = myfile['Scenario'].str.cat(myfile['Test'],sep = " ")
    myfile.columns = ['Type','Scenario','Test','TestName','Combo']

    #making a backup file of cleaned, untokenized information
    mybackupfile = myfile.copy()
    return myfile,mybackupfile


def preprocess(myfile):
    #Tokenizes using NLTK the Scenario column
    myfile['Scenario'] = myfile.apply(lambda column: nltk.word_tokenize(column['Scenario']),axis = 1)
    #tokenizes using NLTK the Test column
    myfile['Test'] = myfile.apply(lambda column: nltk.word_tokenize(column['Test']),axis = 1)
    #tokenizes using NLTK the Combo column
    myfile['Combo'] =myfile.apply(lambda column: nltk.word_tokenize(column['Combo']),axis = 1)

    #removing stopwords from combo
    stopwords=['a','an','and','is','of','its','it']
    myfile['Combo']= myfile['Combo'].apply(lambda x: [item for item in x if item not in stopwords])

        #create corpora in lists
    scenariocorpus = myfile['Scenario'].tolist()
    testcorpus = myfile['Test'].tolist()
    combinedcorpus = myfile['Combo'].tolist()

    #declaring testlen variable (how many tests)
    testlen = len(myfile['Test'])

    return myfile, scenariocorpus,testcorpus,combinedcorpus


def cleanparsefiles(cleanautoroot,cleanmanualroot):
    #gets rid of wonky formatting that includes link to srcml for auto and manual trees
    for child in cleanautoroot:
        child.tag = child.tag.replace('{http://www.srcML.org/srcML/src}','')
        child.tag = child.tag.replace('class','startclass')
        #print(child.tag,child.attrib)
    #print()
    for child in cleanmanualroot:
        child.tag = child.tag.replace('{http://www.srcML.org/srcML/src}','')
        child.tag = child.tag.replace('class','startclass')
        #print(child.tag,child.attrib)

    for tags in cleanautoroot.iter():
        tags.tag = tags.tag.replace('{http://www.srcML.org/srcML/src}','')

    for tags in cleanmanualroot.iter():
        tags.tag = tags.tag.replace('{http://www.srcML.org/srcML/src}','')

def addxmltofile(myfile,cleanmanualroot,cleanautoroot):
    listofmanualfiles = []
    startclassElement = cleanmanualroot.find('startclass/block')
    for element in startclassElement: #isolates comment, function, comment, function for all 
        if (element.tag != 'comment'): #isolates only function blocks
            listofmanualfiles.append(ET.tostring(element, encoding='unicode')) 

    listofautofiles = []
    startclassElement = cleanautoroot.find('startclass/block')
    for element in startclassElement: #isolates comment, function, comment, function for all 
        if (element.tag != 'comment'): #isolates only function blocks
            listofautofiles.append(ET.tostring(element, encoding='unicode')) 

    listofallfiles = []
    listofallfiles = listofmanualfiles + listofautofiles

    #creating uncleaned XML column
    myfile['XML'] = ['' for x in range(len(myfile['Combo']))]
    myfile.columns = ['Type','Scenario','Test','TestName','Combo','XML']
    myfile['XML'] = listofallfiles

    #get rid of keywords
    myfile['XML'] = [entry.replace('4000','') for entry in myfile['XML']]

    #place new root
    for file in range(len(myfile['XML'])):
        myfile['XML'][file] = '<root>' + myfile['XML'][file] + '</root>'
        
    for file in range(len(listofmanualfiles)):
        listofmanualfiles[file] = '<root>' + listofmanualfiles[file] + '</root>'
        
    for file in range(len(listofautofiles)):
        listofautofiles[file] = '<root>' + listofautofiles[file] + '</root>'
        
    for file in range(len(listofallfiles)):
        listofallfiles[file] = '<root>' + listofallfiles[file] + '</root>'

    myfile['XML'] = [entry.replace(r'\n','') for entry in myfile['XML']]
    
    #creating uncleaned XML column
    myfile['Methods'] = ['' for x in range(len(myfile['Combo']))]
    myfile.columns = ['Type','Scenario','Test','TestName','Combo','XML','Methods']
    myfile['Methods'] = listofallfiles
    myfile['Asserts'] = ['' for x in range(len(myfile['Combo']))]
    myfile.columns = ['Type','Scenario','Test','TestName','Combo','XML','Methods', 'Asserts']
    myfile['Asserts'] = listofallfiles
    myfile['Methods_Asserts'] = ['' for x in range(len(myfile['Combo']))]
    myfile.columns = ['Type','Scenario','Test','TestName','Combo','XML','Methods', 'Asserts','Methods_Asserts']
    myfile['Methods_Asserts']=listofallfiles
    myfile['Assert_Only'] = ['' for x in range(len(myfile['Combo']))]
    myfile.columns = ['Type','Scenario','Test','TestName','Combo','XML','Methods', 'Asserts','Methods_Asserts','Assert_Only']
    myfile['Assert_Only']=listofallfiles
    new = []
    for i in range(testlen):
        new.append(i)
    myfile['Index'] = new
    myfile.columns = ['Type','Scenario','Test','TestName','Combo','XML','Methods', 'Asserts','Methods_Asserts','Assert_Only','Index']
    return myfile,listofallfiles

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
    return myfile


def cleancolumns(myfile):
    myfile = clean('Methods')
    myfile = clean('Asserts')
    myfile = clean('Methods_Asserts')
    myfile = clean('Assert_Only')
  
    for file in range(len(myfile['Asserts'])):
        myfile['Asserts'][file] = myfile['Asserts'][file].split()
    for file in range(len(myfile['Methods'])):
        myfile['Methods'][file] = myfile['Methods'][file].split()
    for file in range(len(myfile['Methods_Asserts'])):
        myfile['Methods_Asserts'][file] = myfile['Methods_Asserts'][file].split()
    for file in range(len(myfile['Assert_Only'])):
        myfile['Assert_Only'][file] = myfile['Assert_Only'][file].split()
        
    return myfile

    

    