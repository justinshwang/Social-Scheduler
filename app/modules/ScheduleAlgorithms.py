import random, math, copy, string, ast, time, datetime
from tkinter import*
from modules.image_util import*
from modules.Meet import *

## Programming logic for determining result of inputted time

#Returns dictionary as list with tuple storing information on meeting time and message
def recommendTime(data):
  msg = ""
  #Current time
  currentHour = float(datetime.datetime.now().hour)
  min = datetime.datetime.now().minute
  currentMin = float(min / 60)
  currentTime = currentHour + currentMin
  currentMonth = datetime.date.today().month
  currentDate = datetime.date.today().day
  if data.otherFriends[data.meetName].doNotDisturb == True:
    if data.meetMonth == str(currentMonth) and data.meetDate == str(currentDate):
      #When friend's do not disturb mode is "muted", current time suggested fails
      msg = data.meetName + " is on Do Not Disturb now!\nEvents cannot be scheduled."
      return ("impossible"+ "*" + msg)
  #First checks to see if given time works as suggested
  for event in data.me.calendar.schedule[(data.meetMonth, data.meetDate)]:
    type, priority, start, end, title = event
    if start <= float(data.meetStart) <= end or start <= float(data.meetEnd) <= end:
    #Fails if start or end time falls within another scheduled event
      msg = "This event conflicts with one of\n your own existing events!"
      return ("impossible"+ "*" + msg)
  return closestTime(data)

#Find closest time that works
def closestTime(data):
  #Score equivalent to having overlap of events on both user ends for at least
  #2 events, 10-15 minutes each
  origBestScore = 500
  bestScore = origBestScore
  bestTime = ""
  startUp = float(data.meetStart)
  startDown = float(data.meetEnd)
  difference = float(data.meetEnd) - float(data.meetStart)
  
  #People tend to schedule on the half hour, therefore move by 0.5 interval
  while startUp < 23.5:
    #First check time moving "up" from original inputted time
    startUp += 0.5
    testScore = findScore(data, startUp - difference, difference)
    #A lower score is most optimal
    if testScore < bestScore:
      bestScore = testScore
      bestTime = startUp - difference
  while startDown > 0.5:
    startDown -= 0.5
    testScore = findScore(data, startDown, difference)
    if testScore < bestScore:
      bestScore = testScore
      bestTime = startDown
  if bestScore  == origBestScore:
    msg = "Your event isn't worth scheduling\n today!"
    return ("impossible"+ "*" + msg)
  else:
    return (str(difference) + "*" + (str(bestTime)))
      
#returns a score for the times given
def findScore(data, time, difference):
  overallScore = 0
  scoreMe = 0
  conflicts = 0
  for event in data.me.calendar.schedule[(data.meetMonth, data.meetDate)]:
    visit = 0
    type, priority, start, end, title = event
    testTime = time
    #Tests different times in the appropriate intervals
    while testTime < time + difference:
      if start < testTime  < end:
        #Tracks number of events with conflicts
        if visit == 0:
          conflicts += 1
          visit += 1
        scoreMe += 0.5
      testTime += (1 / 60)  
    #If event had conflict, multiply score by priority value
    if visit == 1:
      scoreMe *= priorityVal(priority)
  if conflicts > 1:
    scoreMe *= 2
      
  scoreFriend = (findFriendScore(data, time, difference))
  
  #Combine two people's scores depending how many conflicts each had
  if scoreFriend != 0 and scoreMe != 0:
    overallScore = 2 * (scoreMe + scoreFriend)
  elif (scoreFriend != 0 and scoreMe == 0) or (scoreMe != 0 and scoreFriend == 0):
    overallScore = 1.5 * (scoreMe + scoreFriend)
  else:
    overallScore = scoreMe + scoreFriend
  
  return overallScore

#finds a friend's score
def findFriendScore(data, time, difference):
  scoreMe = 0
  conflicts = 0
  for event in data.otherFriends[data.meetName].calendar.schedule[(data.meetMonth, data.meetDate)]:
    type, priority, start, end, title = event
    visit = 0
    testTime = time
    while testTime < time + difference:
      if start < testTime  < end:
        #Tracks number of events with conflicts
        if visit == 0:
          conflicts += 1
          visit += 1
        scoreMe += 0.6
      testTime += (1 / 60)  
    #If event had conflict, multiply score by priority value
    if visit == 1:
      scoreMe *= priorityVal(priority)
  if conflicts > 1:
    scoreMe *= 2
  return scoreMe

#Returns values representing importance of priority
def priorityVal(priority):
  score = 0
  # priorityOrder = [None, "social", "eat", "work", "school", "sleep"]
  if priority == None:
    score = 1
  elif priority == "work" or priority == "school":
    score = 5
  elif priority == "sleep":
    score = 4
  elif priority == "eat":
    score = 4
  else:
    score = 2
  
  return score