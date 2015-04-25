from .HHutil import GameType

def hello():
	print("XXXXXXXXXXXX")

def justMatch(userPicks, answers):
	score = 0
	for i in range(0, len(userPicks)):
		if int(userPicks[i]) == int(answers[i]):
			score += 1
	return score

def innpickLogic(userPicks, answers):
	hits = 0
	hitsToScore = {0:2, 1:0, 2:0, 3:0, 4:0, 5:1, 6:1, 7:2, 8:3, 9:4}
	for i in range(1, 10):
		if (i in userPicks) == (i in answers):
			hits += 1
	return hitsToScore[hits]

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

def scoreGame(gameType, entries, answers):
	for user in entries:
		score = 0
		userPicks = entries[user]['selections']
		if gameType in [GameType.RHP, GameType.ABOX]:
			score = justMatch(userPicks, answers)
		elif gameType is GameType.INNP:
			score = innpickLogic(userPicks, answers)
		elif gameType is GameType.OVUN:
			score = overUnder(userPicks, answers)
		elif gameType is GameType.DECL:
			score = declScore(userPicks, answers)
		else:
			pass
		entries[user]['score'] = score
	return entries
