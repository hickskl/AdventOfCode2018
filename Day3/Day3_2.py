import os
import sys
import re
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

def printFabric():
    for row in fabric:
        print (' '.join([str(element) for element in row]))
    print ()

def processClaims():
    for claim in fileData:
        # Extract data (e.g. #    3    @     5   ,    5   :     2   x    2)
        match  = re.search('^#([\\d]+) @ ([\\d]+),([\\d]+): ([\\d]+)x([\\d]+)', claim)
        claim  = int(match.group(1))
        col    = int(match.group(2))
        row    = int(match.group(3))
        width  = int(match.group(4))
        height = int(match.group(5))

        for i in range(col, col+width):
            for j in range(row, row+height):
                if fabric[i][j] != 0: 
                    claimOverlaps.update({claim : True})
                    claimOverlaps[fabric[i][j]] = True                    
                else:
                    fabric[i][j] = claim
                    if claim not in claimOverlaps:
                        claimOverlaps.update({claim : False})

def assessFabric():
    for (claim,overlap) in claimOverlaps.items():
        if not overlap:            
            print ("Claim without Overlap: %d" % claim)

def runTest():
    global fabric, claimOverlaps
    
    # Create fabric
    dimension = 11
    fabric = [[0 for x in range(dimension)] for y in range(dimension)]
    claimOverlaps = defaultdict(lambda : False)

    printFabric()
    processClaims()
    printFabric()
    assessFabric()

def runActual():
    global fabric, claimOverlaps
    
    # Create fabric
    dimension = 1000
    fabric = [[0 for x in range(dimension)] for y in range(dimension)]
    claimOverlaps = defaultdict(lambda : False)
    
    processClaims()
    assessFabric()

setup()
#runTest()   # Test data = input2.txt
runActual()  # Test data = input.txt