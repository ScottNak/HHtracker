import Scripts.HHweekUtil as HH

weekNo = int(input("Week #: "))
thisWeekInfo = HH.runThisWeeksInfo(weekNo)
print("Players this week: " + str(len(thisWeekInfo.keys())))

infoUpToNow = HH.getLastWeeksInfo(weekNo-1)
# newP = 0
# for i in infoUpToNow:
# 	if i not in thisWeekInfo.keys():
# 		newP += 1

# print("New Players this week: " + str(newP))

HH.writeOverallResults(weekNo, thisWeekInfo, infoUpToNow)
