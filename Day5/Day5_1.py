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
    #print(char1,char2)
    if str(char1).lower() == str(char2).lower():
        if ( (str(char1).islower() and str(char2).isupper())
            or (str(char1).isupper() and str(char2).islower()) ):
           react = True
    return react
           
def trimPolymer(unitIndex):
    global polymer

    if i == 0:
        polymer = polymer[i+2:]
    else:
        polymer = polymer[:i] + polymer[i+2:]
    #print(polymer)

setup()

i = 0
while len(polymer) > 1:
    #print (polymer, polymer[i], i, polymer[i+1], i+1)
    while unitsReact(polymer[i], polymer[i+1]):
        trimPolymer(i)
        if i >= len(polymer)-2:
            i = 0
            break
    if i < len(polymer)-2:
        i += 1
    else:
        i = 0
    print (len(polymer))

print(polymer) #9172 delivered via a fantastic infinite loop :c

# Use a stack! Duh. Stack idea:
# https://www.reddit.com/r/adventofcode/comments/a3bruo/2018_day_5_when_optimisation_goes_wrong/eb6lv13/

# unit = 0
# polymerStack = []

# for unit in polymer:
#     #print(unit, polymer, polymerStack)
#     if len(polymerStack) > 0 and unitsReact(polymerStack[-1], unit):
#         polymerStack.pop()
#     else:
#         polymerStack.append(unit)
#     print (len(polymerStack))

# inertPolymer = ''.join([str(unit) for unit in polymerStack])
# print(len(inertPolymer), inertPolymer)