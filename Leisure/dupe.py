import os
import csv
from send2trash import send2trash

## Use Duplicate File Fixer and export selected files to dupe.csv

mainDir = os.getcwd()
print(mainDir)
files = []
with open('dupe.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if row[0] == 'Yes':
            files.append((''.join([row[7],row[2],row[6]])).split("\\"))
##            print(row[2])
##            os.remove(filePath)

##for j in os.listdir(curDir):
##    if '(2)' in j:
##        print(j)

##for i in files:
##    for j in os.listdir(curDir):
##        if i.upper()==j:
##            print(j)
##            send2trash(os.path.join(curDir,j))
dirFixed = []
print(len(files))
for i in files:
    curDir = mainDir
    for j in range(2,len(i)):
        try:
            for k in os.listdir(curDir):
                if i[j].upper() == k.upper():
                    curDir = os.path.join(curDir,k)
                    dirFixed.append(curDir)
##                if os.path.isdir(curDir) == False:
##                    print(os.path.isdir(curDir))
##                    break
        except:
            pass
    print(curDir)
    send2trash(curDir)
