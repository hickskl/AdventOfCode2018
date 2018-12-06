import os
import sys
import re

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

def printFabric():
    print ()
    for row in fabric:
        print (' '.join([str(element) for element in row]))
    print ()
    
    # for row in fabric:
    #     for element in row:
    #         print (element, end=" ")
    #     print()

def processClaims():
    
    for claim in fileData:
        # Extract data from claims (#3 @ 5,5: 2x2)
        match  = re.search('^#(\\d) @ (\\d),(\\d): (\\d)x(\\d)', claim)
        claim  = int(match.group(1))
        col    = int(match.group(2))
        row    = int(match.group(3))
        width  = int(match.group(4))
        height = int(match.group(5))

        #print (claim, col, row, width, height)

        for i in range(col, col+width):
            for j in range(row, row+height):
                fabric[i][j] += 1

def assessFabric():
    

def runTest():
    global fabric
    
    # Create fabric
    dimension = 11
    fabric = [[0 for x in range(dimension)] for y in range(dimension)]

    printFabric()
    processClaims()
    printFabric()
    assessFabric()
    
    print ("Number of Overlapping Inches:", overlapInches)

def runActual():
    global fabric, overlapInches
    
    # Create fabric
    dimension = 1000
    fabric = [[0 for x in range(dimension)] for y in range(dimension)]

    processClaims()
    assessFabric()

    print ("Number of Overlapping Inches:", overlapInches)

setup()

#runTest()   # Test data = input2.txt
runActual()  # Test data = input.txt






