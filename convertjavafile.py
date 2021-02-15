import re
import string
import csv


def main():
    optionbuilderfiles = ["OptionBuilderTest.java", "OptionBuilder_ESTest.java"]
    for file in optionbuilderfiles:
        if "ESTest" in file:
            typetest = "Automatic"
        else: 
            typetest = "Manual"
        print(typetest)
        javafile = open(file,"r")
        found = False
        done = []
        comments = []
        tests = []
        fulltest = []
        comment = True
        firstline = True
        for x in javafile:
            if "public class " in x:
                found = True
                done.append(javafile.read())
                break
        for output in done:
            output = output.replace("/**","*/")
            linesep = output.split("*/")
            for line in linesep:
                if line.isspace() is not True and comment is True and firstline is False:
                    comments.append(line)
                    comment = False
                else:
                    if firstline is False:
                        tests.append(line)
                        comment = True
                firstline = False
        final = []
        counter = 1
        for i in range(len(tests)):
            final.append([str(typetest),comments[i],tests[i]])
  
        with open('outputCSV.csv','w',newline='') as output:
            writer = csv.writer(output)
            writer.writerow(["Type","Scenario","Test"])
            writer.writerows(final)

        with open('outputCSV.csv',newline='') as output:
            reader = csv.reader(output)
            for row in reader:
                print(counter)
                counter+=1
                print(row)
                print()

        final = []
        found = False
        done = []
        comments = []
        tests = []
        fulltest = []
        comment = True
        print()

main()