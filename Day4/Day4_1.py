import os
import sys
import re
import math

class Shift:
    def __init__(self, day, guard):
        self.day = day
        self.guard = guard
        self.onDuty = ['.'] * 60

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

def printSchedule():
    print ("Date   ID     Minute")
    print ("              000000000011111111112222222222333333333344444444445555555555")
    print ("              012345678901234567890123456789012345678901234567890123456789")
    
    for Shift in schedule:
        onDuty = ''.join([str(minute) for minute in Shift.onDuty])
        print ("{0}  #{1}  {2}".format(Shift.day, str(Shift.guard).zfill(4), onDuty))
    print ()

def buildSchedule():
    global schedule
    schedule = []
    newShift = None
    entries = 0

    for entry in fileData:
        entries += 1

        # Extract data (e.g. [  1518-     11-05            00:55]        wakes up)
        match  = re.search('^[[\\d]+-([\\d]+-[\\d]+) ([\\d]+):([\\d]+)] (.*)$', entry)
        date   = match.group(1)
        hour   = int(match.group(2))
        minute = int(match.group(3))
        text   = match.group(4)
        
        if text == "wakes up":
            for i in range(lastTimeChange, minute):
                newShift.onDuty[i] = 'z'
            
            # If we've reached the last shift
            if entries == len(fileData):
                schedule.append(newShift)

        elif text == "falls asleep":
            lastTimeChange = minute

        else: # Set up new shift 
            # Add the last completed shift to the schedule first
            if newShift != None:
                schedule.append(newShift)
             
            match = re.search('Guard #([\\d]+) begins shift', text)
            guard = int(match.group(1))
            
            newShift = Shift(date, guard)

            if hour != 0:
                lastTimeChange = 0
            else:
                lastTimeChange = minute

def processShifts():
    return


setup()
fileData.sort()

buildSchedule()
printSchedule()
processShifts()