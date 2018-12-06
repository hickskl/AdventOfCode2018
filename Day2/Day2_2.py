import os
import sys

def setup():
    global fileHandle, fileData

    filename = input("Enter an input file name: ")
    exists = os.path.isfile("./%s" % filename)
    notEmpty = os.path.getsize("./%s" % filename) > 0

    if exists and notEmpty:
        fileHandle = open ("./%s" % filename, "r")
    else:
        print ("File doesn't exist or is empty.")
        exit
     
    fileData = list()
    for entry in fileHandle:
        fileData.append(entry)
    fileHandle.close()

def stringsDifferByOne(string1, string2):
    global diffPosn
    singleDiffFound = False

    for i in range(len(string1)):
        if string1[i] != string2[i]:
            if singleDiffFound:
                singleDiffFound = False
                break
            else:
                singleDiffFound = True
                diffPosn = i

    return singleDiffFound

setup()

for i in range(len(fileData)):
    for j in range (i, len(fileData)):
        if stringsDifferByOne(fileData[i], fileData[j]):
            checksum = fileData[i][:diffPosn] + fileData[i][diffPosn+1:]
            print("Checksum:", checksum)
            exit