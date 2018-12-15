import os
import sys
import re

class Worker:
    def __init__(self):
        self.job = "."
        self.timeRemaining = 0

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
        match = re.search('Step (\\w) must be finished before step (\\w) can begin.', entry)
        pre   = match.group(1)
        post  = match.group(2)

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

def markJobExecuted(worker):
    global executedSteps, remainingSteps

    remainingSteps.remove(worker.job)
    executedSteps.append(worker.job)

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

def printHeader(workerCount):
    print ("=========================")
    print ("Next", nextSteps)
    print ("Dependent", dependentSteps)
    print ("Starting Stack", instructionStack)
    print ("=========================")

    print ("Second  ", "   ".join(["Elf "+str(x+1) for x in range(workerCount)]), "  Done")

def printStats(step):
    global instructionStack, backlog, remainingSteps, executedSteps

    print ("Stack", instructionStack, "=>", step)
    print ("Backlog", backlog)
    print ("Remaining", remainingSteps)
    print ("Order", executedSteps)
    print ("=========================")

def printSecondSummary(timer):
    global workerQueue, workerCount, executedSteps
    print(" {0}     ".format(str(timer).zfill(4)), "       ".join([workerQueue[i].job for i in range(workerCount)]), "   ", "".join(executedSteps))

def secondsPerStep(step):
    return (ord(step) - 64) + 60 # -64 reduces the ASCII value to A=1, B=2, ...

def isWorking(worker): 
    if worker.job == ".":
        return False
    else: return True

def assignNextJob(worker):
    global instructionStack, workerQueue
    index = workerQueue.index(worker)

    if not isWorking(worker) and len(instructionStack) > 0:
        workerQueue[index].job = instructionStack.pop()
        workerQueue[index].timeRemaining = secondsPerStep(workerQueue[index].job)

def assignInitialJobs():
    global workerQueue

    for worker in workerQueue:
        assignNextJob(worker)

setup()

readInstructions()

firstSteps = findFirstSteps(dependentSteps)     # First steps won't have predecessors
lastStep = findLastStep(nextSteps)              # Last step won't have next steps
instructionStack = firstSteps                   # Preload the stack with the first steps
backlog = [lastStep]                            # Preload the backlog with the last step
executedSteps = []                              # Output
# remainingSteps = [all steps]
stepCount = len(remainingSteps)

workerCount = 5
workerQueue = []
timer = 0

for i in range(workerCount):
    workerQueue.append(Worker())

printHeader(workerCount)
assignInitialJobs()    # Assign the first jobs

# Loop-invariant: only executable steps are in the stack. Non-executable are in the backlog.
# Each cycle processes one second.
while len(remainingSteps) > 0:

    # First process all steps finished last round.
    for i in range(workerCount):
            
        # Process any steps finished last round and reset workers' jobs.
        if isWorking(workerQueue[i]) and workerQueue[i].timeRemaining == 0:
            markJobExecuted(workerQueue[i])
            reviewBacklog()
            pushNextSteps(workerQueue[i].job)
            workerQueue[i].job = "."
            #printStats(workerQueue[i].job)

    # Next, give workers jobs starting from Worker 1.
    for i in range (workerCount):
        assignNextJob(workerQueue[i])
        workerQueue[i].timeRemaining -= 1

    printSecondSummary(timer)
    timer += 1       

if len(executedSteps) == stepCount: # 1099
    print ("Step Order:", ''.join([step for step in executedSteps]), "// Time: {0} seconds".format(int(timer)-1) )
else:
    print ("Error in executing steps.")