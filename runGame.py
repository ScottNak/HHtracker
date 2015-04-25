import Scripts.HHutil as HH
import Scripts.HHscorer as HHSC
import Scripts.HHwriter as HHWR

doPreSiftingList = [HH.GameType.DECL]

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
answers = HH.getAnswerList(gameType, questions)

if gameType in doPreSiftingList:
	pass

markedEntries = HHSC.scoreGame(gameType, goodEntries, answers)
sortedEntries = []
for user in sorted(markedEntries.items(), key=lambda k_v: k_v[1]['score'], reverse=True):
	sortedEntries.append(user)

print("Game Type: " + str(gameType.value))
print("Answers: " + str(answers))

print("All  Entries: ", len(allEntries.keys()))
print("Good Entries: ", len(goodEntries.keys()))
print("Late Entries: ", len(lateEntries), lateEntries)
print("No C Entries: ", len(noCommentList), noCommentList)

xlset = HHWR.makeWBWithSheet()
HHWR.writeResults(gameNo, xlset, gameType, questions, answers, sortedEntries, lateEntries, noCommentList)