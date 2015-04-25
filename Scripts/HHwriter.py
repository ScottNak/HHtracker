from .HHutil import HOME_DIR
from .HHutil import GameType
import xlwt
import os

CORRECT_BGND = xlwt.XFStyle()
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = xlwt.Style.colour_map['lime']
CORRECT_BGND.pattern = pattern

NG_BGND = xlwt.XFStyle()
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = xlwt.Style.colour_map['red']
NG_BGND.pattern = pattern


def makeWBWithSheet():
	wb = xlwt.Workbook()
	sh = wb.add_sheet("Results")
	return (wb, sh)

def writeNormal(sh, Qs, As, userResults):	
	c = 2
	for q in Qs:
		sh.write(0,c, q)
		c += 1

	c = 2
	for a in As:
		sh.write(1,c, a)
		c += 1

	r = 2
	for (user, results) in userResults:
		sh.write(r,0, user)
		sh.write(r,1, results['score'])
		c = 2
		for pick in results['selections']:
			if pick == As[c-2]:
				sh.write(r,c, pick, CORRECT_BGND)
			else:
				sh.write(r,c, pick)
			c+=1
		r+=1	
	return r

def writeOvun(sh, Qs, As, userResults):
	c = 2
	for q in Qs:
		sh.write(0,c, q)
		c += 1	

	c = 2
	for a in As:
		sh.write(1,c, a)
		c += 1

	r = 2
	for (user, results) in userResults:
		sh.write(r,0, user)
		sh.write(r,1, results['score'])
		c = 2
		for pick in results['selections']:
			if results['score'] != 0 and pick == As[c-2]:
				sh.write(r,c, pick, CORRECT_BGND)
			elif results['score'] == 0 and pick != As[c-2] and pick != "PASS":
				sh.write(r,c, pick, NG_BGND)
			else:
				sh.write(r,c, pick)
			c+=1
		r+=1	
	return r

def writeInnp(sh, Qs, As, userResults):
	sh.write(0,2, "Hits")
	c = 3
	for i in range(1, 10):
		sh.write(0,c, i)
		if i in As:
			sh.write(1,c, "Y")
		else:
			sh.write(1,c, "N")
		c += 1	

	r = 2
	for (user, results) in userResults:
		sh.write(r,0, user)
		sh.write(r,1, results['score'][0])
		sh.write(r,2, results['score'][1])
		c = 3
		pick = results['selections']			
		for i in range(1, 10):
			userPick = "Y" if (i in pick) else "N"
			if (i in pick) == (i in As):
				sh.write(r, c, userPick, CORRECT_BGND)
			else:
				sh.write(r, c, userPick)
			c+=1
		r+=1	
	return r



def writeResults(num, xlSet, GT, Qs, As, userResults, ngList, noCommList):
	(wb, sh) = xlSet

	sh.write(0,0, GT.name)
	sh.write(0,1, "Score")
	sh.write(1,0, "Answer")

	r = 77
	if GT in [GameType.RHP, GameType.ABOX]:
		r = writeNormal(sh, Qs, As, userResults)	
	elif GT is GameType.OVUN:
		r = writeOvun(sh, Qs, As, userResults)
	elif GT is GameType.INNP:
		r = writeInnp(sh, Qs, As, userResults)

	c = (3+9) if GT is GameType.INNP else (2 + len(As))
	for ng in ngList:
		sh.write(r, 0, ng)
		sh.write(r, 1, "X", NG_BGND)
		sh.write_merge(r, r, 2, c-1, "LATE")
		r+=1

	for ng in noCommList:
		sh.write(r, 0, ng)
		sh.write(r, 1, "X", NG_BGND)
		sh.write_merge(r, r, 2, c-1, "NO COMMENT")
		r+=1	

	if num < 10:
		num = "00" + str(num)
	elif num < 100:
		num = "0" + str(num)
	else:
		num = str(num)
	wb.save("./Results/Game" + num + "out.xls")
	os.startfile(HOME_DIR + "/Results/Game" + num + "out.xls")