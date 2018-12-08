import os
import sys
import re

class Shift:
    def __init__(self, day, guard):
        self.day = day
        self.guard = guard
        #self.onDuty = ['.'] * 60 # minutes
        self.onDuty = [0] * 60 # minutes

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
    print ()
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

        # Extract data (e.g. [  1518-     11-05            00:55      ]  wakes up)
        match  = re.search('^.[\\d]+-([\\d]+)-([\\d]+) ([\\d]+):([\\d]+). (.*)$', entry)
        month  = int(match.group(1))
        day    = int(match.group(2))
        hour   = int(match.group(3))
        minute = int(match.group(4))
        text   = match.group(5)
        
        if text == "wakes up":
            for i in range(lastTimeChange, minute):
                #newShift.onDuty[i] = 'z'
                newShift.onDuty[i] = 1  # 0 awake, 1 asleep
            
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

            # Shift the day by 1 if the shift starts before 00:00
            if hour != 0:
                day += 1 

            date = "{0}-{1}".format(str(month).zfill(2), str(day).zfill(2))
            newShift = Shift(date, guard)

def processShifts():
    sleepiestGuard = 0
    sleepiestMinute = 0
    sleepiestSum = 0

    sumOfGuardShifts = {} # { key=guard : value=sum of minutes in shift)

    # Zip up each guard's shifts into one shift summary
    for Shift in schedule:
        if Shift.guard not in sumOfGuardShifts:
            sumOfGuardShifts.update({Shift.guard : Shift.onDuty})
        else:
            sumMinutes = [sum(x) for x in zip(Shift.onDuty, sumOfGuardShifts[Shift.guard])]
            sumOfGuardShifts[Shift.guard] = sumMinutes

        #print (Shift.guard, ' '.join([str(minute) for minute in sumOfGuardShifts[Shift.guard]]))

    # Parse through each minute to find which guard sleeps the most
    # Keep track of the most-slept minute and guard number
    for min in range (60):
        for (guard,shift) in sumOfGuardShifts.items():
            if shift[min] > sleepiestSum:
                sleepiestGuard = guard
                sleepiestSum = shift[min]
                sleepiestMinute = min

    print ("Guard", sleepiestGuard, "slept the more during minute", sleepiestMinute, "for {0} shifts.".format(sleepiestSum))
    print ("Checksum:", int(sleepiestGuard * sleepiestMinute))

setup()
fileData.sort()

buildSchedule()
printSchedule()
processShifts()