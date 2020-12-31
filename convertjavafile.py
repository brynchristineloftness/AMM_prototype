import re
import string
import csv


def main():
    optionbuilderfiles = ["OptionBuilder_ESTest.java"]
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
        for x in javafile:
            if "public class " in x:
                found = True
                done.append(javafile.read())
                break
        for output in done:
            output = output.replace("/**","*/")
            linesep = output.split("*/")
            for line in linesep:
                if line.isspace() is not True and comment is True:
                    comments.append(line)
                    comment = False
                else:
                    tests.append(line)
                    comment = True
        final = []
        for i in range(len(comments)):
            final.append([str(typetest),comments[i],tests[i]])
  
        with open('CommandLineCSV.csv','w',newline='') as output:
            writer = csv.writer(output)
            writer.writerow(["Type","Scenario","Test"])
            writer.writerows(final)

        with open('CommandLineCSV.csv',newline='') as output:
            reader = csv.reader(output)
            for row in reader:
                print(row)
                print()

        final = []
        found = False
        done = []
        comments = []
        tests = []
        fulltest = []
        comment = True

main()