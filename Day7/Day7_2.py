import os
import sys
import re

def setup():
    global fileHandle, fileData

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
    
    fileData = []
    for line in fileHandle:
        fileData.append(line.rstrip())
    fileHandle.close()

def readInstructions():
    global nextSteps, dependentSteps, remainingSteps
    nextSteps = {}          # { X : [steps after step X]}
    dependentSteps = {}     # { X : [steps X is dependent on]}
    remainingSteps = []

    for entry in fileData:
        match  = re.search('Step (\\w) must be finished before step (\\w) can begin.', entry)
        pre  = match.group(1)
        post = match.group(2)

        if pre not in nextSteps:
            nextSteps.update({ pre : [post] })
        else:
            nextSteps[pre].append(post)

        if post not in dependentSteps:
            dependentSteps.update({ post : [pre] })
        else:
            dependentSteps[post].append(pre)

        # Build list of all steps to execute
        remainingSteps.append(pre)
        remainingSteps.append(post)
        
    remainingSteps = sorted(set(remainingSteps))

def findFirstSteps(list):
    global remainingSteps
    temp = []

    for step in remainingSteps:
        if step not in list:
            temp.append(step)
    
    temp.sort(reverse=True)
    return temp                 # One or more first steps

def findLastStep(list):
    global remainingSteps
    
    for step in remainingSteps:
        if step not in list:
            return step         # Just one last step

def markStepExecuted(step):
    global executedSteps

    remainingSteps.remove(step)
    executedSteps.append(step)

def readyToExecute(step):
    global dependentSteps, remainingSteps
    predecessorsExecuted = True

    for predecessor in dependentSteps[step]:
        if predecessor in remainingSteps:
            predecessorsExecuted = False

    return predecessorsExecuted

def reviewBacklog():
    global backlog, instructionStack
    
    for step in backlog:
        if readyToExecute(step):
            backlog.remove(step)
            if step not in instructionStack:
                instructionStack.append(step)

def pushNextSteps(step):
    global lastStep, nextSteps, instructionStack, backlog

    if step == lastStep:    # Nothing to do for last step
        return

    # Push onto the stack if ready to execute, otherwise push
    # into the backlog to be reviewed next execution cycle.
    for next in nextSteps[step]:
        if readyToExecute(next):
            if next not in instructionStack:
                instructionStack.append(next)
            if next in backlog:
                backlog.remove(next)
        elif next not in backlog:
            backlog.append(next)
            
    # Stack must remain sorted, unique and filled with executable steps only.
    instructionStack.sort(reverse=True)

setup()

readInstructions()

firstSteps = findFirstSteps(dependentSteps)     # First steps won't have predecessors
lastStep = findLastStep(nextSteps)              # Last step won't have next steps
instructionStack = firstSteps                   # Preload the stack with the first steps
backlog = [lastStep]                            # Preload the backlog with the last step
executedSteps = []                              # Output
stepCount = len(remainingSteps)
# remainingSteps = all steps

print ("=========================")
print ("Next", nextSteps)
print ("Dependent", dependentSteps)
print ("Starting Stack", instructionStack)

# Loop-invariant: only executable steps are in the stack. Non-executable are in the backlog.
while len(remainingSteps) > 0:
    print ("=========================")
    step = instructionStack.pop()
    markStepExecuted(step)
    reviewBacklog()
    pushNextSteps(step)

    print ("Stack", instructionStack, "=>", step)
    print ("Backlog", backlog)
    print ("Remaining", remainingSteps)
    print ("Order", executedSteps)

print ("=========================")
if len(executedSteps) == stepCount:
    print ("Step Order:", ''.join([step for step in executedSteps]))
else:
    print ("Error in executing steps.")