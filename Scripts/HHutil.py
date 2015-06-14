import xlrd
import datetime
import os
import re
import urllib.request
import json
import sys
import webbrowser
from enum import Enum

HOME_DIR = "C:/Users/ScottNak/Documents/HHtracker/"
HH_LINK = 'http://www.halosheaven.com/pregame-thread'
HH_GET_LINK = "http://www.sbnrollcall.com/XHR/fetchBlog.php?action=fetchBlog&urls[]="
MLB_LINK = "mlb.mlb.com/mlb/gameday/index.jsp?gid=2015_{:02}_{:02}_{}_{}_1&mode=box"
CHROME_DIR = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
LINKS = re.compile("<a.* href=\"(.*)\">Game\s?(\d+).*</a>")

CONVERT_TO_URL = { 'Angels': 'anamlb','Royals': 'kcamlb','Athletics': 'oakmlb','Rangers': 'texmlb','Mariners': 'seamlb',
'Astros': 'houmlb','Rockies': 'colmlb','Padres': 'sdnmlb','Tigers': 'detmlb','Rays': 'tbamlb','D-backs': 'arimlb',
'Yankees': 'nyamlb','Red Sox': 'bosmlb','Twins': 'minmlb','Indians': 'clemlb','Orioles': 'balmlb','White Sox': 'chamlb',
'Blue Jays': 'tormlb','Dodgers': 'lanmlb','Giants': 'sfnmlb'}

class GameType(Enum):
	RHP  = 1
	ABOX = 2
	OVUN = 3
	INNP = 4
	DECL = 5
	BLJK = 6

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
	date = xlrd.xldate.xldate_as_datetime(schedSH.cell_value(num, 0), schedWB.datemode)
	match = schedSH.cell_value(num, 4).split(" at ")
	print(MLB_LINK.format(date.month, date.day, CONVERT_TO_URL[match[0]], CONVERT_TO_URL[match[1]]))
	webbrowser.get(CHROME_DIR).open(MLB_LINK.format(date.month, date.day, CONVERT_TO_URL[match[0]], CONVERT_TO_URL[match[1]]), new=1)
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

def grabCommentHelper(url):
	print(" >>>> Requesting >>>> " + url)
	resp = urllib.request.urlopen(url)
	info = resp.read().decode("utf-8")
	print(json.loads(info)['data']['commentsByCommenter'])
	users = json.loads(info)['data']['commentsByCommenter'].keys()
	print(" >>>> DONE >>>> ")
	return users

def getCommentUsers(num):
	try:
		resp = urllib.request.urlopen(HH_LINK)
		info = resp.read().decode("utf-8")
		url2 = ''	
		for (gameURL, gameNo) in LINKS.findall(info):				
			if(int(gameNo) == num):
				url2 = HH_GET_LINK + gameURL
				break
		return grabCommentHelper(url2)
	except:
		webbrowser.get(CHROME_DIR).open(HH_LINK, new=1)
		urlNew = HH_GET_LINK + input("Unable to find a proper link. Try manually: ")
		return grabCommentHelper(urlNew)		

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
	elif returnMe[0] == "The \"Cards\"":
		gameType = GameType.BLJK
	else:
		print("Unable to detect game type. Pick from list")
		for i in GameType:
			print("  " + str(i.value) + ": " + str(i.name))
		gameType = GameType(int(input("Use This: ")))

	return (gameType, returnMe)

def getAnswerList(GT, Qs, presiftInfo):
	isOK = False
	ans = []
	while not isOK:
		ans = []
		if GT == GameType.INNP:
			ans = input("Innings with Runs: ")
			ans = [int(x) for x in ans.split(" ")]
		elif GT == GameType.DECL:
			ans = {}
			for key in presiftInfo:
				ans[key] = {}
				for feat in presiftInfo[key]:
					val = int(input(key + ", " + feat + " = "))
					ans[key][feat] = val
		elif GT == GameType.BLJK:
			ans = {}
			for card in presiftInfo:
				val = int(input(card + " = "))
				ans[card] = val
		else:
			for qq in Qs:
				reply = input("Answer to " + qq + ": ")
				if is_number(reply):
					ans.append(int(reply))
				else:
					ans.append(reply)
		isOK = input("OK? ") != "n"
	return ans

def getEntries(WB, SH):
	returnMe = {}
	for r in range(1, SH.nrows):
		thisEntryTime = datetime.datetime(*xlrd.xldate_as_tuple(SH.cell_value(r,0), WB.datemode)) 
		thisUser = str(int(SH.cell_value(r, 1))) if SH.cell_type(r,1) == 2 else SH.cell_value(r, 1)
		thisUser = thisUser.strip()
		thisSelections = []
		for c in range(2, SH.ncols):
			thisEntry = SH.cell_value(r, c)
			if (SH.cell_type(r,c) == 2): #number
				thisEntry = int(thisEntry)
			thisSelections.append(thisEntry)
		returnMe[thisUser] = {'time': thisEntryTime, 'selections': thisSelections}
	return returnMe

def presiftDECL(userPicks):
	shortcut = {}
	for user in userPicks:
		selection = userPicks[user]['selections']
		checks = shortcut.get(selection[0], [])
		if selection[3] not in checks:
			checks.append(selection[3])
		shortcut[selection[0]] = checks

	return shortcut

def presiftBLJK(userPicks):
	shortcut = ['[*] LAA H']
	for user in userPicks:
		selection = userPicks[user]['selections'][0].split(", ")
		for s in selection:
			if s not in shortcut:
				shortcut.append(s)
	return sorted(shortcut)
