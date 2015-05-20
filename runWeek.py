import Scripts.HHweekUtil as HH

weekNo = int(input("Week #: "))
thisWeekInfo, weekLeader = HH.runThisWeeksInfo(weekNo)
infoUpToNow = HH.getLastWeeksInfo(weekNo-1)
overallLeader = HH.writeOverallResults(weekNo, thisWeekInfo, infoUpToNow)

print("Players this week: " + str(len(thisWeekInfo.keys())))

HH.trackLeaders(weekNo, weekLeader, overallLeader)
