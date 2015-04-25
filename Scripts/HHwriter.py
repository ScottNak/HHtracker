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

def writeResults(num, xlSet, GT, Qs, As, userResults, ngList, noCommList):
	(wb, sh) = xlSet

	sh.write(0,0, GT.name)
	sh.write(0,1, "Score")
	c = 2
	for q in Qs:
		sh.write(0,c, q)
		c += 1

	sh.write(1,0, "Answer")
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
	wb.save("Game" + num + "out.xls")
	os.startfile("Game" + num + "out.xls")