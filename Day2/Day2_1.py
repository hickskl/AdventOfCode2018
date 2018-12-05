import os
import sys
from collections import defaultdict

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

setup()

twoTupleCount = 0
threeTupleCount = 0
letterMap = defaultdict(int)

for label in fileData:

    for letter in label:
        letterMap [letter] += 1

    for key,val in letterMap.items():
        if val == 2:
            twoTupleCount += 1
            break

    for key,val in letterMap.items():
        if val == 3:
            threeTupleCount += 1
            break

    letterMap.clear()

checksum = twoTupleCount * threeTupleCount
print ("Checksum:", checksum)
