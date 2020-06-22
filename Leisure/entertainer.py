import os
import sys
import shutil
import gspread
import xlsxwriter
from oauth2client.service_account import ServiceAccountCredentials


class film(object):
	name = ''
	year = 0
	subs = False
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

def makeNewFilm(curDir, dirName, sub):
	dNs = dirName.split()
	f = film()
	f.year = int(dNs.pop()[1:5])
	f.name = ' '.join(dNs)
	f.subs = sub
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
		films.write(i, 0, f.name)
		films.write(i, 1, f.year)
		if f.subs: films.write(i, 2, 'Sub')
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
				print(clean)
				os.rename(i, clean)
				shutil.move(clean, filmDir)
			except:
				print('ERROR: Could not rename', i)
	os.chdir(curDir)

def nameFix():
		MOVIE_EXT = ['mp4', 'mkv', 'avi']
		SUB_EXT = ['sub', 'srt', 'idx', 'smi']
		curDir = os.getcwd()
		# filmDir = os.path.join(curDir, 'Films')
		# filmsExisting = os.listdir(filmDir)
		holdDir = os.path.join(curDir, 'Holding')

		for i in os.listdir(holdDir):
				path = os.path.join(holdDir, i)
				contents = os.listdir(path)
				film = [j for j in contents if j.split('.')[-1] in MOVIE_EXT]
				subs = [k for k in contents if k.split('.')[-1] in SUB_EXT]
				dirs = [l for l in contents if os.path.isdir(os.path.join(path, l))]
				if dirs : print('EXTRANEOUS FOLDERS IN', path)
				if len(contents) > len(film) + len(subs) : print('EXTRANEOUS FILES IN', path)
				if len(film) > 1:
						print('MORE THAN ONE MOVIE FILE IN', path)
						continue
				elif not film:
						print('NO MOVIE FILE FOUND IN', path)
						continue
				film_ext = '.' + film[0].split('.')[-1]
				os.rename(os.path.join(path, film[0]), os.path.join(path, i + film_ext))
				print(os.path.join(path, film[0]), os.path.join(path, i + film_ext))

				if len(subs) > 1:
						print('MORE THAN ONE SUBTITLE FILE IN', path)
						continue
				elif not subs:
						#print('NO SUBTITLE FOR', path)
						continue
				subs_ext = '.' + subs[0].split('.')[-1]
				os.rename(os.path.join(path, subs[0]), os.path.join(path, i + '.en' + subs_ext))

				#print(os.path.join(path, subs[0]), os.path.join(path, i + '.en' + subs_ext))
				#print(path)

##        print(dir[0])
##        print(os.listdir(os.path.join(filmDir, dir[0])))
##        dir2 = os.listdir(os.path.join(filmDir, dir[0]))
##        os.rename(os.path.join(os.path.join(filmDir, dir[0]), dir2[0]), os.path.join(os.path.join(filmDir, dir[0]), dir[0] + '.mp4'))
##        for path, subdirs, files in os.walk(os.getcwd()):
##                for i in files:
##                        ext = i.split('.')[-1]
##                        if ext in ['mp4', 'mkv', 'avi']:
##                                #print(os.path.join(path, i))
##                                print(path.split(os.sep)[-1])
##                                #os.rename(os.path.join(path, i), os.path.join(path, path.split(os.sep)[-1]))
##                                #continue
##                        elif ext == 'jpg':
##                                print('image', os.path.join(path, i))
##                                os.remove(os.path.join(path, i))
##                        elif ext in ['sub', 'srt', 'idx', 'smi']:
##                                #print('subs', os.path.join(path, i))
##                                continue
##                        else:
##                                print('other', os.path.join(path, i))
##                                os.remove(os.path.join(path, i))

def films():
		SUB_EXT = ['sub', 'srt', 'idx', 'smi']
		curDir = os.path.join(os.getcwd(), 'Films')
		dirList = [d for d in os.listdir(curDir) if os.path.isdir(os.path.join(curDir, d))]
		fList = []
		for f in dirList:
				sub = True if [k for k in os.listdir(os.path.join(curDir, f)) if k.split('.')[-1] in SUB_EXT] else False
				fList.append(makeNewFilm(curDir, f, sub))
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
	# connect to Google Drive
	scope = ['https://spreadsheets.google.com/feeds',
			 'https://www.googleapis.com/auth/drive']
	credentials = ServiceAccountCredentials.from_json_keyfile_name(mainDir+'\client_secret.json', scope)
	gc = gspread.authorize(credentials)

	# initialize sheet and remove temp sheets
	sh = gc.open('Entertainment')
	lst = sh.worksheets()
	try:
		sh.del_worksheet(sh.worksheet('Films.temp'))
	except:
		pass
	try:
		sh.del_worksheet(sh.worksheet('Shows.temp'))
	except:
		pass

	# parse films
	frows = len(fL)
	wk = sh.add_worksheet(title='Films.temp', rows=frows, cols=2)
	name_range = wk.range('A1:A'+str(frows))
	year_range = wk.range('B1:B'+str(frows))
	# subs_range = wk.range('C1:C'+str(rows))
	#for i in range(len(fL)):
	for n, i in enumerate(fL):
		name_range[n].value = i.name
		year_range[n].value = i.year
		# if i.subs: subs_range[n].value = 'Subbed'
		# print(i.name, i.year, i.subs)
	wk.update_cells(name_range)
	wk.update_cells(year_range)
	# wk.update(name_range)
	# wk.update(year_range)
	# wk.batch_update([name_range, year_range])
	# wk.update_cells(subs_range)
	sh.del_worksheet(sh.worksheet('Films'))
	wk.update_title(title='Films')

	# parse shows
	srows = len(sL)
	wk = sh.add_worksheet(title='Shows.temp', rows=srows, cols=26)
	for n, i in enumerate(sL):
		row = chr(n+65)
		range = wk.range(row+'1:'+row+str(len(i.seasons)+1))
		range[0].value = i.name
		# wk.update_cell(n+1, 1, i.name)
		for m, j in enumerate(i.seasons):
			range[m+1].value = j
			# wk.update_cell(n+1, m+2, j)
		wk.update_cells(range)
	sh.del_worksheet(sh.worksheet('Shows'))
	wk.update_title(title='Shows')

def main(argv):
	# mainDir = os.getcwd()
	mainDir = argv[0]
	os.chdir(mainDir)
	print(mainDir)
	dirFix()
	nameFix()
	fL = films()
	sL = shows()
	writeXLSX(fL, sL)
	gsheets(mainDir, fL, sL)
	print(len(fL), 'movies,', len(sL), 'shows')
##	input("Press Enter to exit...")

def test(argv):
		mainDir = argv[0]
		os.chdir(mainDir)
		print(mainDir)
		filmNameFix()

if __name__ == "__main__":
		main(sys.argv[1:])
