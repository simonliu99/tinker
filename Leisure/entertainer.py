import os
import sys
import shutil
import gspread
import xlsxwriter
from oauth2client.service_account import ServiceAccountCredentials


class film(object):
	name = ''
	year = 0
	# broke = False

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
	f.status = dirStatus(curDir, dirName)
	return f

def makeNewShow(dirName, seasons):
	s = show()
	s.name = dirName
	s.seasons = seasons
	return s

def dirStatus(curDir, dirName):
	if os.listdir(os.path.join(curDir, dirName)) == []:
		return 'red'
	for dirpath, dirnames, filenames in os.walk(os.path.join(curDir, dirName)):
		for filename in filenames:
			if not filename.endswith('mp4') and not filename.endswith('mkv') and not filename.endswith('srt') and not filename.endswith('_Sub') and not filename.endswith('avi') and not filename.endswith('idx') and not filename.endswith('_Subs') and not filename.endswith('sub') and not filename.endswith('_Subtitles') and not filename.endswith('smi'):
				return 'yellow'
	return ''

def writeXLSX(fL, sL):
	book = xlsxwriter.Workbook('Entertainment.xlsx')

	films = book.add_worksheet('Films')
	maxLen = 0
	for i, f in enumerate(fL):
		form, formC = formats(book, f.status)
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

def dirFix():
	# curDir = os.path.join(mD, 'Films')
	curDir = os.getcwd()
	holdDir = os.path.join(curDir, 'Holding')
	filmDir = os.path.join(curDir, 'Films')
	os.chdir(holdDir)
	dirList = [d for d in os.listdir(holdDir) if os.path.isdir(os.path.join(holdDir, d))]
	for i in dirList:
		dirSplit = i.split()
		checked = False
		for j, k in enumerate(dirSplit):
			if k[0] == '(' and k[-1] == ')' and str.isdigit(k[1:-2]):
				clean = ' '.join(i.split()[:j + 1])
				del dirSplit[j + 1:]
				checked = True
		if not checked:
			print('ERROR: Inconsistent naming', i)
		elif os.path.exists(os.path.join(filmDir, clean)):
			print('ERROR: Film already exists', i)
		else:
			try:
				# print('SUCCESS', clean)
				os.rename(i, clean)
				shutil.move(clean, filmDir)
			except:
				print('ERROR: Could not rename', i)
	os.chdir(curDir)

def films():
	curDir = os.path.join(os.getcwd(), 'Films')
	dirList = [d for d in os.listdir(curDir) if os.path.isdir(os.path.join(curDir, d))]
	fList = []
	for f in dirList:
		fList.append(makeNewFilm(curDir, f))
	fList.sort(key=lambda f:f.name)
	return fList

def shows():
	curDir = os.path.join(os.getcwd(), 'Shows')
	dirList = [d for d in os.listdir(curDir) if os.path.isdir(os.path.join(curDir, d))]
	sList = []
	for s in dirList:
		curSub = os.path.join(curDir, s)
		subList = [u for u in os.listdir(curSub) if os.path.isdir(os.path.join(curSub, u))]
		sList.append(makeNewShow(s, subList))
	sList.sort(key=lambda s:s.name)
	return sList

def gsheets(mainDir, fL, sL):
	scope = ['https://spreadsheets.google.com/feeds',
			 'https://www.googleapis.com/auth/drive']

	credentials = ServiceAccountCredentials.from_json_keyfile_name(mainDir+'\client_secret.json', scope)

	gc = gspread.authorize(credentials)

	sh = gc.open('Entertainment')
	lst = sh.worksheets()
	try:
		sh.del_worksheet(sh.worksheet('Movies.temp'))
	except:
                pass
	try:
		sh.del_worksheet(sh.worksheet('Shows.temp'))
	except:
                pass

	wk = sh.add_worksheet(title='Movies.temp', rows=1000, cols=26)
	name_range = wk.range('A1:A'+str(len(fL)))
	year_range = wk.range('B1:B'+str(len(fL)))
	for i in range(len(fL)):
		name_range[i].value = fL[i].name
		year_range[i].value = fL[i].year
	wk.update_cells(name_range)
	wk.update_cells(year_range)
	sh.del_worksheet(sh.worksheet('Movies'))
	wk.update_title(title='Movies')

	wk = sh.add_worksheet(title='Shows.temp', rows=1000, cols=26)
	for n, i in enumerate(sL):
		wk.update_cell(n+1, 1, i.name)
		for m, j in enumerate(i.seasons):
			wk.update_cell(n+1, m+2, j)
	sh.del_worksheet(sh.worksheet('Shows'))
	wk.update_title(title='Shows')

def main(argv):
	# mainDir = os.getcwd()
	mainDir = argv[0]
	os.chdir(mainDir)
	print(mainDir)
	dirFix()
	fL = films()
	sL = shows()
	writeXLSX(fL, sL)
	gsheets(mainDir, fL, sL)
	print(len(fL), 'movies,', len(sL), 'shows')
##	input("Press Enter to exit...")

if __name__ == "__main__":
	main(sys.argv[1:])
