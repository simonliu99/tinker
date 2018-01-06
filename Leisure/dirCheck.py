import os
from os import listdir, walk
from os.path import isfile, join
os.chdir('/Volumes/Alpha/Leisure/Entertainment')

f = []
for (dirpath, dirnames, filenames) in walk(os.getcwd()):
    f.extend(filenames)

exts = []
j = []
for i in f:
    ext = i.split('.')[-1]
    if ext not in exts:
        exts.append(ext)
        j.append(i)
print(exts)
print(' ')
print(j)
