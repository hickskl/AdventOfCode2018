import os
import sys
import math
import itertools

def setup():
    global fileHandle, coordinates, maxX, maxY

    filename = input("Enter an input file name (default input2.txt): ")
    if filename == "":
        filename = "input2.txt"

    exists = os.path.isfile("./%s" % filename)
    notEmpty = os.path.getsize("./%s" % filename) > 0

    if exists and notEmpty:
        fileHandle = open ("./%s" % filename, "r")
    else:
        print ("File doesn't exist or is empty.")
        exit
    
    maxX = 0
    maxY = 0
    coordinates = []

    for line in fileHandle:
        temp = line.rstrip().split(",")
        coordinates.append( ( int(temp[0]), int(temp[1]) ) )
        
        # Save the max X and Y coordinate values
        if int(temp[0]) > maxX:
            maxX = int(temp[0])
        if int(temp[1]) > maxY:
            maxY = int(temp[1])
    
    # Adjust for origin
    maxX += 1
    maxY += 1

    fileHandle.close()

def printGrid():
    for row in grid:
        print (''.join([str(element) for element in row]))
    print ()

def plotPoints():
    for (label,(x,y)) in enumerate(coordinates):
        grid[y][x] = label

def manhattanDistance(posn1, posn2):
    return abs(posn1[0] - posn2[0]) + abs(posn1[1] - posn2[1])

def plotSafeRegion(safeRegionArea):
    x = 0
    y = 0
    inSafeRegion = 0

    for (x,y) in itertools.product(range(maxX), range(maxY)):
        totalDistance = 0

        for location in coordinates:
            totalDistance += manhattanDistance((x,y), location)
        
        if totalDistance < safeRegionArea:
            inSafeRegion += 1 
            grid[y][x] = 'S'  

    return inSafeRegion

def runTest():
    safeRegionArea = 32

    plotPoints()
    printGrid()
    print("Calculating safe region...")
    safeCount = plotSafeRegion(safeRegionArea)
    printGrid()
    print("Size of Safe Region:", safeCount)

def runActual():
    safeRegionArea = 10000

    plotPoints()
    print("Calculating safe region...")
    safeCount = plotSafeRegion(safeRegionArea)
    print("Size of Safe Region:", safeCount)

setup()
global grid
grid = [['.' for x in range(maxX)] for y in range(maxY)]

#runTest() # 16
runActual() # 45176

