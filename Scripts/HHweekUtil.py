import xlrd

def getLastWeeksInfo(num):
	if num == 0:
		return {}
	elif num < 10:
		num = "0" + str(num)
	else:
		num = str(num)
	wb = xlrd.open_workbook(HOME_DIR + 'Weeks/Week' + num + ".xlsx")
	ws = wb.sheet_by_index(0)

	return gatherInfo(ws)

def gatherInfo(ws):
	gameType = sh.
	for r in range(2, ws.nrows):
		user = sh.cell_value(r, 0).strip()
		score = sh.cell_value(r, 1)



	