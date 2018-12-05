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

freqList = list()
for freqChange in file:
    freqList.append(int(freqChange))
file.close()

freq = 0
found = False
foundFreqList = list()

startTime = time.time()
while found != True:        
    for freqChange in freqList:
        freq += freqChange

        if freq in foundFreqList:
            found = True
            break
        else:
            foundFreqList.append(freq)      

print (time.time() - startTime) #127.36426 sec
print ("First frequency found twice: %d" % freq)