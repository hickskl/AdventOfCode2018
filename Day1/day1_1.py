import os
import sys

filename = input("Enter an input file name: ")

exists = os.path.isfile("./%s" % filename)

if exists:
    file = open ("./%s" % filename, "r")
else:
    print ("File doesn't exist")
    exit

freq = 0

for line in file:
    if line is not None:
        #print ("%d" % int(line))
        freq = freq + int(line)
    else:
        print ("Reached EOF")

file.close()

print ("Sum of frequency changes: %d" % freq)