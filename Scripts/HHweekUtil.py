import xlrd
import xlwt
import os
from .HHutil import HOME_DIR
from .HHwriter import makeWBWithSheet

weekToGameStart = {1:1, 2:6, 3:12, 4:19, 5:25, 6:32, 7:37, 8:44, 9:51, 10: 57, 11:63, 12:70, \
				  13:76,14:82, 15:89, 16:98, 17:104, 18:110, 19:117, 20:124, 21:130, 22:136, \
				  23:142, 24:149, 25:155, 26: 163}

def getLastWeeksInfo(num):
	if num == 0:
		return {}
	elif num < 10:
		num = "0" + str(num)
	else:
		num = str(num)
	wb = xlrd.open_workbook(HOME_DIR + 'Overall/Overall' + num + ".xls")
	ws = wb.sheet_by_index(0)

	return gatherInfo(ws)

def gatherInfo(ws):
	lastResult = {}
	for r in range(1, ws.nrows):
		thisUser = str(int(ws.cell_value(r, 0))) if ws.cell_type(r,0) == 2 else ws.cell_value(r, 0)
		thisUser = thisUser.strip()
		thisScore = int(ws.cell_value(r, 1))
		thisPlay = int(ws.cell_value(r, 2))
		thisHistory = []		
		for c in range(3, ws.ncols):
			val = int(ws.cell_value(r, c)) if ws.cell_type(r,c) == 2 else ws.cell_value(r, c)
			thisHistory.append(val)
		lastResult[thisUser.lower()] = {'name': thisUser, 'score': thisScore, 'play': thisPlay, 'history': thisHistory}
	return lastResult

def runThisWeeksInfo(weekNo):	
	start = weekToGameStart[weekNo]
	end = weekToGameStart[weekNo+1]
	returnMe = {}
	whichGame = {}
	for num in range(start, end):
		print(" ========= Game # " + str(num))
		if num < 10:
			x = "00" + str(num)
		elif num < 100:
			x = "0" + str(num)
		else:
			x = str(num)
		print(num)
		wb = xlrd.open_workbook(HOME_DIR + 'Results/Game' + x + "out.xls")
		sh = wb.sheet_by_index(0)
		whichGame[num] = sh.cell_value(0,0)		
		for r in range(2, sh.nrows):
			user = str(int(sh.cell_value(r, 0))) if sh.cell_type(r,0) == 2 else sh.cell_value(r, 0)
			user = user.strip()
			score = sh.cell_value(r, 1)			
			if score == "X":
				break
			else:
				score = int(score)
			userInfo = returnMe.get(user.lower(), {'name': user, 'scores': ['-']*(end-start)})
			userInfo['scores'][num-start] = score
			returnMe[user.lower()] = userInfo
	leaderInfo = writeThisWeek(returnMe, whichGame, weekNo, start, end)
	return (returnMe, leaderInfo)

def getUserScoreInfo(ptArray):
	mySum = 0
	myPlay = 0
	for i in ptArray:
		if i is not "-":
			mySum += i
			myPlay += 1
	return (mySum, myPlay)
	

def getSortValue(ptArray):
	(mySum, myPlay) = getUserScoreInfo(ptArray)
	return mySum*100+myPlay

		
def writeThisWeek(weekInfo, whichGame, weekNo, start, end):
	(wb, sh) = makeWBWithSheet()
	sh.write(1,0, "User")
	sh.write(1,1, "PTS")
	sh.write(1,2, "PLAY")
	for i in range(start, end):
		sh.write(0, 3+(i-start), i)
		sh.write(1, 3+(i-start), whichGame[i])
		
	r = 2

	sortedEntries = []
	for user in sorted(weekInfo.items(), key=lambda k_v: getSortValue(k_v[1]['scores']), reverse=True):
		sortedEntries.append(user[1])

	hiScore = None
	hiScoreList = []
	for userInfo in sortedEntries:
		sh.write(r,0, userInfo['name'])
		(userScore, userPlay) = getUserScoreInfo(userInfo['scores'])
		sh.write(r,1, userScore)
		sh.write(r,2, userPlay)

		if hiScore is None:
			hiScore = userScore

		if userScore is hiScore:
			hiScoreList.append(userInfo['name'])

		for i in range(start, end):
			sh.write(r, 3+(i-start), userInfo['scores'][i-start])
		r+= 1

	weekNo = "0" + str(weekNo) if weekNo < 10 else str(weekNo)
	wb.save("./Weeks/Week" + weekNo + ".xls")
	os.startfile(HOME_DIR + "/Weeks/Week" + weekNo + ".xls")	

	return (hiScoreList, hiScore)

def writeOverallResults(weekNo, thisWkInfo, pastInfo):
	(wb, sh) = makeWBWithSheet()
	sh.write(0,0, "Player")
	sh.write(0,1, "PTS")
	sh.write(0,2, "PLAY")
	for i in range(0, weekNo):
		sh.write(0,3+i, i+1)

	overallData = {}
	for user in thisWkInfo:		
		(userScore, userPlay) = getUserScoreInfo(thisWkInfo[user]['scores'])
		prevPts = ['-'] * weekNo
		prevPts[weekNo-1] = userScore

		if user in pastInfo:
			pastUserInfo = pastInfo[user]
			prevPts = pastUserInfo['history'] + [userScore]
			userScore += pastUserInfo['score']
			userPlay += pastUserInfo['play']			
				
		overallData[user] = {'name': thisWkInfo[user]['name'], 'score': userScore, 'play': userPlay, 'history': prevPts}
	for user in pastInfo:
		if user not in thisWkInfo:
			overallData[user] = {'name': pastInfo[user]['name'], 'score': pastInfo[user]['score'], \
								 'play': pastInfo[user]['play'], 'history': pastInfo[user]['history'] + ['-']}

	sortedEntries = []
	for user in sorted(overallData.items(), key=lambda k_v: k_v[1]['score'], reverse=True):
		sortedEntries.append(user[1])	

	r = 1
	hiScore = None
	hiScoreList = []
	for user in sortedEntries:
		sh.write(r, 0, user['name'])
		sh.write(r, 1, user['score'])
		sh.write(r, 2, user['play'])

		if hiScore is None:
			hiScore = user['score']

		if user['score'] is hiScore:
			hiScoreList.append(user['name'])

		for c in range(1, weekNo+1):
			sh.write(r, 3+c-1, user['history'][c-1])
		r += 1

	weekNo = "0" + str(weekNo) if weekNo < 10 else str(weekNo)
	wb.save("./Overall/Overall" + weekNo + ".xls")
	os.startfile(HOME_DIR + "/Overall/Overall" + weekNo + ".xls")	

	return (hiScoreList, hiScore)

def trackLeaders(gNo, weekL, overallL):
	print(">>>>>>>>>>>>>>")
	print("Weekly  Leader: " + ', '.join(weekL[0]))
	print("Weekly  Score : " + str(weekL[1]))
	print(">>>>>>>>>>>>>>")
	print("Overall Leader: " + ', '.join(overallL[0]))
	print("Overall Score : " + str(overallL[1]))
	print(">>>>>>>>>>>>>>")

	f = open(HOME_DIR+"/runningLeaders.txt", 'a')
	f.write("[{:0>2d}] {} || {}\n".format(gNo, ', '.join(weekL[0]), ', '.join(overallL[0])))
	f.close()