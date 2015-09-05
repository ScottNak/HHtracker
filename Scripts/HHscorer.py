from .HHutil import GameType
from .HHutil import is_number

def justMatch(userPicks, answers):
	score = 0
	for i in range(0, len(userPicks)):
		userAns = int(userPicks[i]) if is_number(userPicks[i]) else userPicks[i]
		answer  = int(answers[i]) if is_number(answers[i]) else answers[i]

		if userAns == answer:
			score += 1
	return score

def innpickLogic(userPicks, answers):
	hits = 0
	hitsToScore = {0:2, 1:0, 2:0, 3:0, 4:0, 5:1, 6:1, 7:2, 8:3, 9:4}

	for i in range(1, 10):
		if (i in userPicks) == (i in answers):
			hits += 1
	return (hitsToScore[hits], hits)

def overUnder(userPicks, answers):
	score = 0
	for i in range(0, len(userPicks)):
		if userPicks[i] != "PASS":
			if userPicks[i] == answers[i]:
				score += 1
			else:
				return 0
	return score

def declScore(userPicks, answers):
	playerPos = userPicks[0]
	isAtLeast = userPicks[1] == "at least (+0)"
	numericVal= userPicks[2]
	theFeat	  = userPicks[3]
	possScore = numericVal + (0 if isAtLeast else 2)
	if isAtLeast:
		return possScore if answers[playerPos][theFeat] >= numericVal else 0
	else:
		return possScore if answers[playerPos][theFeat] == numericVal else 0

def bljkScore(userPicks, answers):
	picks = userPicks[0].split(", ")
	score = answers['[*] LAA H']
	print(score)
	for p in picks:
		score += answers[p]
	if score is 17 or score is 18:
		ptsGet = 1
	elif score is 19 or score is 20:
		ptsGet = 2
	elif score is 21:
		ptsGet = 4
	else:
		ptsGet = 0

	return ptsGet + score/100

def bingoScore(userPicks, answers):
	print (answers)
	print (userPicks)
	blots = []
	for i in range(0, 9):
		blots.append(userPicks[i].startswith("Gets a") == answers[i])
		print(userPicks[i])

	print(str(blots[0]) + " " + str(blots[1]) + " " + str(blots[2]))
	print(str(blots[3]) + " " + str(blots[4]) + " " + str(blots[5]))
	print(str(blots[6]) + " " + str(blots[7]) + " " + str(blots[8]))

	score = 0
	if (blots[0] and blots[1] and blots[2]):
		score += 1
	if (blots[3] and blots[4] and blots[5]):
		score += 1
	if (blots[6] and blots[7] and blots[8]):
		score += 1
	if (blots[0] and blots[3] and blots[6]):
		score += 1
	if (blots[1] and blots[4] and blots[7]):
		score += 1
	if (blots[2] and blots[5] and blots[8]):
		score += 1
	if (blots[0] and blots[4] and blots[8]):
		score += 1
	if (blots[2] and blots[4] and blots[6]):
		score += 1

	print("Score: " + str(score))
	return score


def scoreGame(gameType, entries, answers):
	for user in entries:
		score = 0

		userPicks = entries[user]['selections']
		if gameType in [GameType.RHP, GameType.ABOX]:
			score = justMatch(userPicks, answers)
		elif gameType is GameType.INNP:			 
			if not is_number(userPicks[0]):
				entries[user]['selections'] = [int(x) for x in userPicks[0].split(", ")]
			score = innpickLogic(entries[user]['selections'], answers)
		elif gameType is GameType.OVUN:
			score = overUnder(userPicks, answers)
		elif gameType is GameType.DECL:
			score = declScore(userPicks, answers)
		elif gameType is GameType.BLJK:
			score = bljkScore(userPicks, answers)
		elif gameType is GameType.BINGO:
			score = bingoScore(userPicks, answers)
		else:
			pass
		entries[user]['score'] = score
	return entries
