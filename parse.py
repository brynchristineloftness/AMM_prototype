from imports import *

def isolatemethods_asserts(myfile,listofallfiles):
    #isolating methods and assertions

    counter = 0
    for file in listofallfiles:
        stringstuff = ''
        assertstuff = ''
        expressionstuff = ''
        finalassertname = ''
        namestring = ''
        rootspot = ET.fromstring(file)
        findfunction = rootspot.find('function/block/block_content')
        tagstring = (ET.tostring(findfunction,encoding = 'unicode'))
        #print(tagstring)
        for element in findfunction:
            if (element.tag == 'decl_stmt'):
                for el in element:
                    if el.tag == 'decl':
                        for item in el:
                            if item.tag == 'init':
                                for call in item:
                                    if call.tag == 'expr':
                                        for name in item:
                                            if name.tag == 'expr':
                                                for item in name:
                                                    for call in item:
                                                        if call.tag == 'name':
                                                            methods_notrycatch_noasserts = (ET.tostring(call,encoding = 'unicode'))
                                                            stringstuff+=methods_notrycatch_noasserts
                                                            expressionstuff +=methods_notrycatch_noasserts
            elif(element.tag=='try'):
                tagstring = (ET.tostring(element,encoding = 'unicode'))
                for item in element:
                    if item.tag=='block':
                        for block in item:
                            if block.tag =='block_content':
                                for trystmt in block:
                                    if trystmt.tag == 'expr_stmt':
                                        for element in trystmt:
                                            if element.tag=='expr':
                                                for expr in element:
                                                    if expr.tag =='call':
                                                        for child in expr:
                                                            if child.tag == 'name':
                                                                trystuff = (ET.tostring(child,encoding = 'unicode'))
                                                                stringstuff += trystuff
                                                                expressionstuff += trystuff
            elif(element.tag == 'expr_stmt'):
                for element2 in element:
                    if element2.tag == 'expr':
                        for expr in element2:
                            if expr.tag == 'call':
                                for call in element:
                                    if call.tag == 'expr':
                                        for expr in call:
                                            if expr.tag =='call':
                                                for file in expr:
                                                    if file.tag == 'name':
                                                        assertname = (ET.tostring(file,encoding = 'unicode'))
                                                        assertstuff += assertname
                                                        expressionstuff += assertname
                                                        finalassertname = assertname
                                                    elif file.tag =='argument_list':
                                                        for element in file:
                                                            if element.tag == 'argument':
                                                                for item in element:
                                                                    if item.tag == 'expr':
                                                                        for child in item:
                                                                            if child.tag == 'call':
                                                                                for children in child:
                                                                                    if children.tag == 'name':
                                                                                        for name in children:
                                                                                            if name.tag =='name':
                                                                                                namespot = (ET.tostring(name,encoding = 'unicode'))
                                                                                                assertstuff += namespot
                                                                                                expressionstuff+=namespot

        myfile['Methods'][counter] = stringstuff
        myfile['Asserts'][counter] = assertstuff
        myfile['Methods_Asserts'][counter] = expressionstuff
        myfile['Assert_Only'][counter] = finalassertname
        counter += 1
    return myfile

