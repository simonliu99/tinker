import os
import sys
import xlsxwriter

class film(object):
    name = ''
    year = 0

class show(object):
    name = ''
    seasons = []

def makeNewFilm(dirName):
    dNs = dirName.split()
    dNlen = dNs.__len__()
    f = film()
    f.year = int(dNs.pop()[1:5])
    f.name = ' '.join(dNs)
    return f

def makeNewShow(dirName,seasons):
    s = show()
    s.name = dirName
    seasonList = []
    s.seasons = seasons
    return s

def writeXLSX(fL,sL):
    book = xlsxwriter.Workbook('Entertainment.xlsx')
    font = book.add_format({'font_name':'Courier','font_size':12})
    center = book.add_format({'font_name':'Courier','font_size':12,'align':'center'})
    
    films = book.add_worksheet('Films')
    maxLen = 0
    for i,f in enumerate(fL):
        films.write(i,0,f.name,font)
        films.write(i,1,f.year,center)
        maxLen = len(f.name) if len(f.name) > maxLen else maxLen
    films.set_column(0,0,maxLen+12)

    shows = book.add_worksheet('Shows')
    maxLen = 0
    maxSeason = 0
    for j,s in enumerate(sL):
        shows.write(j,0,s.name,font)
        maxLen = len(s.name) if len(s.name) > maxLen else maxLen
        for k,n in enumerate(s.seasons):
            shows.write(j,k+1,n,center)
            maxSeason = len(s.seasons) if len(s.seasons) > maxSeason else maxSeason
    shows.set_column(0,0,maxLen+10)
    shows.set_column(1,maxSeason,20)

    book.close()

def dirFix(mD):
    curDir = os.path.join(mD,'Films')
    os.chdir(curDir)
    dirList = [d for d in os.listdir(curDir) if os.path.isdir(os.path.join(curDir, d))]
    for i in dirList:
        dirSplit = i.split()
        checked = False
        while checked != True:
            if dirSplit[-1][0] == '[' and dirSplit[-1][-1] == ']':
                print(dirSplit[-1]),
                dirSplit.pop()
                print(' '.join(dirSplit))
            else:
                checked = True
        try:
            os.rename(i,' '.join(dirSplit))
        except:
            print('Could not rename:', i)
    os.chdir(mD)
    input("Press Enter to continue...")
        
def films(mD):
    curDir = os.path.join(mD,'Films')
    dirList = [d for d in os.listdir(curDir) if os.path.isdir(os.path.join(curDir, d))]
    fList = []
    for f in dirList:
        fList.append(makeNewFilm(f))
    return fList

def shows(mD):
    curDir = os.path.join(mD,'Shows')
    dirList = [d for d in os.listdir(curDir) if os.path.isdir(os.path.join(curDir, d))]
    sList = []
    for s in dirList:
        curSub = os.path.join(curDir,s)
        subList = [u for u in os.listdir(curSub) if os.path.isdir(os.path.join(curSub, u))]
        sList.append(makeNewShow(s,subList))
    return sList

def main():
    mainDir = os.getcwd()
    print(mainDir)
    dirFix(mainDir)
    fL = films(mainDir)
    sL = shows(mainDir)
    writeXLSX(fL,sL)
    print(len(fL),'movies,',len(sL),'shows')
    input("Press Enter to exit...")

main()
