import os
import xlsxwriter

class film(object):
    name = ''
    year = 0
    broke = False

class show(object):
    name = ''
    seasons = []

def formats(b, color):
    font = b.add_format({'font_name': 'Courier', 'font_size': 12})
    center = b.add_format({'font_name': 'Courier', 'font_size': 12, 'align': 'center'})
    if color == '':
        return font, center
    cFont = b.add_format({'font_name': 'Courier', 'font_size': 12, 'bg_color': color})
    cFontC = b.add_format({'font_name': 'Courier', 'font_size': 12, 'align': 'center', 'bg_color': color})
    return cFont, cFontC

def makeNewFilm(curDir, dirName):
    dNs = dirName.split()
    f = film()
    f.year = int(dNs.pop()[1:5])
    f.name = ' '.join(dNs)
    f.broke = (os.listdir(os.path.join(curDir, dirName)) == [])
    print(f.broke)
    return f

def makeNewShow(dirName, seasons):
    s = show()
    s.name = dirName
    s.seasons = seasons
    return s

def writeXLSX(fL, sL):
    book = xlsxwriter.Workbook('Entertainment.xlsx')

    films = book.add_worksheet('Films')
    maxLen = 0
    for i, f in enumerate(fL):
        if f.broke:
            form, formC = formats(book, 'red')
        else:
            form, formC = formats(book, '')
        films.write(i, 0, f.name, form)
        films.write(i, 1, f.year, formC)
        maxLen = len(f.name) if len(f.name) > maxLen else maxLen
    films.set_column(0, 0, maxLen + 12)

    shows = book.add_worksheet('Shows')
    maxLen = 0
    maxSeason = 0
    form, formC = formats(book, '')
    for j, s in enumerate(sL):
        shows.write(j, 0, s.name, form)
        maxLen = len(s.name) if len(s.name) > maxLen else maxLen
        for k, n in enumerate(s.seasons):
            shows.write(j, k + 1, n, formC)
            maxSeason = len(s.seasons) if len(s.seasons) > maxSeason else maxSeason
    shows.set_column(0, 0, maxLen + 10)
    shows.set_column(1, maxSeason, 20)

    book.close()

def dirFix(mD):
    curDir = os.path.join(mD, 'Films')
    os.chdir(curDir)
    dirList = [d for d in os.listdir(curDir) if os.path.isdir(os.path.join(curDir, d))]
    for i in dirList:
        dirSplit = i.split()
        checked = False
        for j, k in enumerate(dirSplit):
            if k[0] == '(' and k[-1] == ')':
                del dirSplit[j + 1:]
                checked = True
        if not checked:
            print('ERROR:', i)
        else:
            try:
                os.rename(i, ' '.join(dirSplit))
            except:
                print('ERROR: Could not rename', i)
    os.chdir(mD)

def films(mD):
    curDir = os.path.join(mD, 'Films')
    dirList = [d for d in os.listdir(curDir) if os.path.isdir(os.path.join(curDir, d))]
    fList = []
    for f in dirList:
        fList.append(makeNewFilm(curDir, f))
    return fList

def shows(mD):
    curDir = os.path.join(mD, 'Shows')
    dirList = [d for d in os.listdir(curDir) if os.path.isdir(os.path.join(curDir, d))]
    sList = []
    for s in dirList:
        curSub = os.path.join(curDir, s)
        subList = [u for u in os.listdir(curSub) if os.path.isdir(os.path.join(curSub, u))]
        sList.append(makeNewShow(s, subList))
    return sList

def main():
    os.chdir('/Volumes/Alpha/Entertainment')
    mainDir = os.getcwd()
    print(mainDir)
    dirFix(mainDir)
    fL = films(mainDir)
    sL = shows(mainDir)
    writeXLSX(fL, sL)
    print(len(fL), 'movies,', len(sL), 'shows')
    input("Press Enter to exit...")

main()
