import os
import sys

def setup():
    global fileHandle, polymer

    filename = input("Enter an input file name: ")
    exists = os.path.isfile("./%s" % filename)
    notEmpty = os.path.getsize("./%s" % filename) > 0

    if exists and notEmpty:
        fileHandle = open ("./%s" % filename, "r")
    else:
        print ("File doesn't exist or is empty.")
        exit
     
    polymer = fileHandle.read().rstrip()
    fileHandle.close()

def unitsReact(char1, char2):
    react = False
    if str(char1).lower() == str(char2).lower():
        if ( (str(char1).islower() and str(char2).isupper())
            or (str(char1).isupper() and str(char2).islower()) ):
           react = True
    return react

def processPolymer(letter):
    for unit in polymer:
        if unit.lower() == letter.lower():
            continue
        elif len(polymerStack) > 0 and unitsReact(polymerStack[-1], unit):
            polymerStack.pop()
        else:
            polymerStack.append(unit)

    inertPolymer = ''.join([str(unit) for unit in polymerStack])
    print (letter, "->", len(inertPolymer))

    unitMap.update({letter : len(inertPolymer)})
    polymerStack.clear()

setup()

unit = 0
polymerStack = []
unitMap = {}        # { letter : reacted polymer with letter removed }

for letter in sorted(set(polymer.lower())): # "set" removes duplicates
    processPolymer(letter)    

print ( "Smallest polymer: %d" % min(unitMap.values()) )
