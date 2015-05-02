import Scripts.HHutil as HH

gameNo = int(input("Week #: "))
thisWeekSet = HH.getThisWeeksWB(gameNo-1)
infoUpToNow = {} if thisWeekSet is not None else HH.extractWeek(thisWeekSet)

print(infoUpToNow)