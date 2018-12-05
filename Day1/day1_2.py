import os
import sys
import time

filename = input("Enter an input file name: ")

exists = os.path.isfile("./%s" % filename)
notEmpty = os.path.getsize("./%s" % filename) > 0

if exists and notEmpty:
    file = open ("./%s" % filename, "r")
else:
    print ("File doesn't exist or is empty.")
    exit

found = False
freq = 0
foundFreqList = list()

startTime = time.time()
while found != True:
    for freqChange in file:
        freq += int(freqChange)

        if freq in foundFreqList:
            found = True
            break
        else:
            foundFreqList.append(freq)      

    file.close()
    file = open ("./%s" % filename, "r")

file.close()

print (time.time() - startTime) #127.86179 sec
print ("First frequency found twice: %d" % freq)