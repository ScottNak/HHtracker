import xlwt
import xlrd
import datetime
import os
import re
import urllib.request
import json
import sys
from enum import Enum

HOME_DIR = "C:/Users/ScottNak/Documents/HHtracker/"
HH_LINK = 'http://www.halosheaven.com/pregame-thread'
HH_GET_LINK = "http://www.sbnrollcall.com/XHR/fetchBlog.php?action=fetchBlog&urls[]="
LINKS = re.compile("<a.* href=\"(.*)\">Game\s?(\d+).*</a>")

class GameType(Enum):
	RHP  = 1
	ABOX = 2
	OVUN = 3
	INNP = 4
	DECL = 5

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def getThisGamesWB(num):
	if num < 10:
		num = "00" + str(num)
	elif num < 100:
		num = "0" + str(num)
	else:
		num = str(num)
	wb = xlrd.open_workbook(HOME_DIR + 'Games/Game' + num + " (Responses).xlsx")
	ws = wb.sheet_by_index(0)
	return (wb, ws)

def getThisGameTimeLimit(num):
	schedWB = xlrd.open_workbook(os.path.abspath(HOME_DIR+'schedule.xlsx'))
	schedSH = schedWB.sheet_by_index(0)
	return confirmTimeOK(xlrd.xldate.xldate_as_datetime(schedSH.cell_value(num, 0), schedWB.datemode))

def confirmTimeOK(limit):
	needsNew = limit.time() == datetime.time(3,33)
	
	if needsNew:
		print("[!] Schedule file has 3:33AM, update needed! ")
	else:
		resp = input("This time ok? <" + str(limit) + ">: " )
		needsNew = not (resp == "" or resp != "y" or resp != "Y")

	while needsNew:
		resp = input("Enter time: ")
		resp = [int(x) for x in resp.split(":")]
		limit = limit.replace(hour=resp[0], minute=resp[1])
		resp = input("New Cutoff is <" + str(limit) + "> OK? ")
		needsNew = not (resp == "" or resp != "y" or resp != "Y")

	return limit

def getCommentUsers(num):
	try:
		resp = urllib.request.urlopen(HH_LINK)
		info = resp.read().decode("utf-8")
		url2 = ''	
		for (gameURL, gameNo) in LINKS.findall(info):				
			if(int(gameNo) == num):
				url2 = HH_GET_LINK + gameURL
				break
		print(" >>>> Requesting >>>> ")
		resp = urllib.request.urlopen(url2)
		info = resp.read().decode("utf-8")
		users = json.loads(info)['data']['commentsByCommenter'].keys()
		print(" >>>> DONE >>>> ")
		return users
	except:
		print( "Uh oh... " + sys.exc_info())

def getGameInfo(WB, SH):
	returnMe = []
	for c in range(2, SH.ncols):
		returnMe.append(SH.cell_value(0, c))

	gameType = "?"
	if returnMe[0] == "LAA R":
		gameType = GameType.RHP
	elif "[A]" in returnMe[0] and "[B]" in returnMe[0]:
		gameType = GameType.ABOX
	elif "Margin of Victory" in returnMe[-1]:
		gameType = GameType.OVUN
	elif "Innings with a run by either team" in returnMe[0]:
		gameType = GameType.INNP
	elif returnMe == ["[ A ]", "[ B ]", "[ C ]", "[ D ]"]:
		gameType = GameType.DECL
	else:
		print("Unable to detect game type. Pick from list")
		for i in GameType:
			print("  " + str(i.value) + ": " + str(i.name))
		gameType = GameType(int(input("Use This: ")))

	return (gameType, returnMe)

def getAnswerList(GT, Qs):
	ans = []
	if GT == GameType.INNP:
		ans = input("Innings with Runs: ")
		ans = [int(x) for x in ans.split(" ")]
	elif GT == GameType.DECL:
		ans = []
	else:
		for qq in Qs:
			reply = input("Answer to " + qq + ": ")
			if is_number(reply):
				ans.append(int(reply))
			else:
				ans.append(reply)
	return ans

def getEntries(WB, SH):
	returnMe = {}
	for r in range(1, SH.nrows):
		thisEntryTime = datetime.datetime(*xlrd.xldate_as_tuple(SH.cell_value(r,0), WB.datemode)) 
		thisUser = str(int(SH.cell_value(r, 1))) if SH.cell_type(r,1) == 2 else SH.cell_value(r, 1)
		thisSelections = []
		for c in range(2, SH.ncols):
			thisEntry = SH.cell_value(r, c)
			if (SH.cell_type(r,c) == 2): #number
				thisEntry = int(thisEntry)
			thisSelections.append(thisEntry)
		returnMe[thisUser] = {'time': thisEntryTime, 'selections': thisSelections}
	return returnMe

def getAnswers(gameType, returnMe):
	isOk = False
	while not isOk:
		answers = []
		if gameType in [GameType.RHP, GameType.ABOX, GameType.OVUN]:
			for i in returnMe:
				answers.append(input("Answer to: [" + i + "]: "))
			for i in range(0, len(answers)):
				print (returnMe[i] + ": " + answers[i])
		elif gameType is GameType.INNP:
			answers = input("Innings with Runs: ").split(" ")
			print ("Answer: " + str(answers))
		elif gameType is GameType.DECL:
			pass

		isOk = input("OK? ") != "n"
	return (gameType, answers)
