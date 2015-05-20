import Scripts.HHutil as HH
import Scripts.HHscorer as HHSC
import Scripts.HHwriter as HHWR

gameNo = int(input("Game #: "))
thisGameLimit = HH.getThisGameTimeLimit(gameNo)
thisGameWB, thisGameSH = HH.getThisGamesWB(gameNo)
userCommentList = HH.getCommentUsers(gameNo)

allEntries = HH.getEntries(thisGameWB, thisGameSH)

verifiedEntries = {k:v for (k,v) in allEntries.items() if k.lower() in [x.lower() for x in userCommentList]}
noCommentList = [k for (k,v) in allEntries.items() if k.lower() not in [x.lower() for x in userCommentList]]
goodEntries = {k:v for (k, v) in verifiedEntries.items() if (v['time'] <= thisGameLimit)}
lateEntries = [k for (k, v) in verifiedEntries.items() if (v['time'] > thisGameLimit)]

(gameType, questions) = HH.getGameInfo(thisGameWB, thisGameSH)
presiftInfo = None
if gameType is HH.GameType.DECL:
	presiftInfo = HH.presiftDECL(goodEntries)
elif gameType is HH.GameType.BLJK:
	presiftInfo = HH.presiftBLJK(goodEntries)
	print(presiftInfo)
print(presiftInfo)
answers = HH.getAnswerList(gameType, questions, presiftInfo)

markedEntries = HHSC.scoreGame(gameType, goodEntries, answers)
sortedEntries = []
print(sorted(markedEntries.items(), key=lambda x: x[1]['score'], reverse=True))
for user in sorted(sorted(markedEntries.items(), key=lambda x: x[0]), key=lambda y: y[1]['score'], reverse=True):
	sortedEntries.append(user)

print("Game Type: " + str(gameType.name))
print("Answers: " + str(answers))

print("All  Entries: ", len(allEntries.keys()))
print("Good Entries: ", len(goodEntries.keys()))
print("Late Entries: ", len(lateEntries), lateEntries)
print("No C Entries: ", len(noCommentList), noCommentList)

xlset = HHWR.makeWBWithSheet()
HHWR.writeResults(gameNo, xlset, gameType, questions, answers, sortedEntries, lateEntries, noCommentList)