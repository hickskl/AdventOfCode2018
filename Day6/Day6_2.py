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

def areaIsFinite(area):
    finite = True
    
    # An area is infinite if it has a point on the border of the grid.
    for x in range(maxX):
        if grid[0][x] == area or grid[maxY-1][x] == area:
            finite = False
    
    for y in range(maxY):
        if grid[y][0] == area or grid[y][maxX-1] == area:
            finite = False
    
    return finite

def calculateArea(label):
    size = 0
    for (x,y) in itertools.product(range(maxX), range(maxY)):
        if grid[y][x] == label:
            size += 1
    return size

def plotClosestLocations():
    x = 0
    y = 0
    closestLocation = 0

    for (x,y) in itertools.product(range(maxX), range(maxY)):    # For each point in the grid
        for (label,location) in enumerate(coordinates):          # For each input coord. pair
            distance = manhattanDistance((x,y), location)
            if label == 0:
                closestLocation = distance      # Set a default location
                grid[y][x] = label
            elif distance == closestLocation:   # Tied with another location
                grid[y][x] = '.'
            elif distance < closestLocation:    # Current location is closer to (x,y)
                closestLocation = distance
                grid[y][x] = label

def findLargestFiniteArea():
    largestArea = 0
    for (label,location) in enumerate(coordinates):
        if areaIsFinite(label):
            area = calculateArea(label)
            if area > largestArea:
                largestArea = area
                print("Area", label, location, "->", area)

    print ("Largest Area:", largestArea)

setup()

global grid
grid = [['.' for x in range(maxX)] for y in range(maxY)]

plotPoints()
#printGrid()
print("Assigning grid points to locations...")
plotClosestLocations()
#printGrid()
print("---Finite Areas---")
findLargestFiniteArea()