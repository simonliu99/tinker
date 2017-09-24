import os
import xlrd
import xlwt

class movie(object):
    name = ''
    year = 0

def makeNewMovie(dirName):
    dNs = dirName.split()
    dNlen = dNs.__len__()
    m = movie()
    m.year = int(dNs.pop()[1:5])
    m.name = ' '.join(dNs)
    return m

def makeMovie(n,y):
    m = movie()
    m.name = n
    m.year = int(y)
    return m

def writeXLS(mL):
    book = xlwt.Workbook()
    sh = book.add_sheet('Movies')
    maxLen = 0
    for i,m in enumerate(mL):
        sh.write(i,0,m.name)
        sh.write(i,1,m.year)
        maxLen = len(m.name) if len(m.name) > maxLen else maxLen
    #sh.set_column(1, 1, maxLen + 5)
    book.save('MoviesTemp.xls')

def readXLS(fN):
    book = xlrd.open_workbook(fN)
    sh = book.sheet_by_index(0)
    mL = []
    for j in range(0,sh.nrows):
        mL.append(makeMovie(sh.cell(j,0).value,sh.cell(j,1).value))
    return mL
        
def main():
    os.chdir('G:\\Movies')
    curDir = os.getcwd()
    print curDir
    mListInit = readXLS('Movies.xls')
    dirList = [d for d in os.listdir(curDir) if os.path.isdir(os.path.join(curDir, d))]
    mList = []
    print ' '
    for m in dirList:
        mX = makeNewMovie(m)
        mU = True
        for mI in mListInit:
            mU = False if mX.name == mI.name else mU
        mList.append(mX) if mU == True else mU
    mList.extend(mListInit)
    os.remove('Movies.xls')
    writeXLS(mList)
    os.rename('MoviesTemp.xls','Movies.xls')

main()
