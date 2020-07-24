import random, math, copy, string
from tkinter import*
from image_util import*
from Meet import *
from GeneralAppFunctioning import*

priorityOrder = [None, "social", "eat", "work", "school", "sleep"]

####################################
# Function specific to Meet Application
####################################

def init(data):
  ##EDIT
  calendar = "schedule2.txt"
  name = "Justin"
  disturb = False
  #
  disturb = False
  data.me = Profile(name, disturb, calendar)
  data.otherFriends = dict()
  data.mode = "Home"
  data.optionsMode = "Closed"
  
  #Meet mode
  data.meetMonth = input("MONTH")
  data.meetDate = input("DATE")
  data.meetStart = input("START Time")
  data.meetEnd = input("ENDTIME")
  data.meetPriority = input("PRIORITY")
  data.meetMsg = input("MESSAGE")
  data.msg = ""
  
  #Tab icons       
  data.meetImage = PhotoImage(file="meet.gif")
  data.homeImage = PhotoImage(file="home.gif")
  data.calImage = PhotoImage(file="calendar.gif")
  
  #Success tab animation
  data.tabAnimate = False
  data.recommendAnimate = False
  data.tabOpen = True
  data.successTabY = 0
  data.fadeSuccessTab = 99
  data.fadeRecommendTab = 99
  data.tabTime = 0
  data.recommendation = ""
      
  #Friends schedule
  data.friend = Profile("Eric", False, "schedule1.txt")
  data.scheduleOther = data.friend.calendar.schedule

  r, m = recommendTime(data).split("*")
  print(r)
  print(m)
  
## Test scheduling algorithms


#Returns dictionary as list with tuple storing information on meeting time and message
def recommendTime(data):
  msg = ""
  #First checks to see if given time works as suggested
  for event in data.me.calendar.schedule[(data.meetMonth, data.meetDate)]:
    type, priority, start, end, title = event
    if start <= float(data.meetStart) <= end or start <= float(data.meetEnd) <= end:
    #Fails if start or end time falls within another scheduled event
      msg = "Your event conflicts with one of\n your own existing events!"
      #return closestTime(data)!!
      return ("impossible"+ "*" + msg)
  return closestTime(data)
  
#Find closest time that works
def closestTime(data):
  origBestScore = 500
  bestScore = origBestScore
  bestTime = ""
  startUp = float(data.meetStart)
  startDown = float(data.meetEnd)
  difference = float(data.meetEnd) - float(data.meetStart)
  searching = True
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
      
#returns a score for the time
def findScore(data, time, difference):
  overallScore = 0
  scoreMe = 0
  conflicts = 0
  for event in data.me.calendar.schedule[(data.meetMonth, data.meetDate)]:
    visit = 0
    type, priority, start, end, title = event
    testTime = time
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
  ##EDIT data.scheduleOther
  for event in data.scheduleOther[(data.meetMonth, data.meetDate)]:
    type, priority, start, end, title = event
    visit = 0
    testTime = time
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
    score = 2
  else:
    score = 3
  
  return score

def mousePressed(event, data):
  msg = ""
  x, y = event.x, event.y

  margin = data.width / 10
  diX = data.width - data.width / 10
  diY = data.width / 5
  tabHeight = data.height - data.height / 8
  if diX - margin < x < diX + margin and diY - margin < y < diY + margin:
    #If do not disturb button is pressed, change mode
    data.me.doNotDisturb = not data.me.doNotDisturb
    msg = "disturb" + " " + data.me.name  + "\n"
  elif 0 <= x < data.width / 3 and tabHeight <= y <= data.height:
    #Change mode to calendar
    data.mode = "Calendar"
  elif data.width / 3 <= x < 2 * data.width / 3 and tabHeight <= y <= data.height:
    #Change mode to Home
    data.mode = "Home"
  elif data.width * 2 / 3 <= x <= data.width and tabHeight <= y <= data.height:
    #Change mode to Meet
    data.mode = "Meet"
  
  if data.mode == "Home":
    homeMousePressed(event, data)
  elif data.mode == "Calendar":
    calMousePressed(event, data)
  elif data.mode == "Meet":
    meetMousePressed(event,data)

def keyPressed(event, data):
  if event.keysym == "q":
    pass
    
  if data.mode == "Home":
    homeKeyPressed(event, data)
  elif data.mode == "Calendar":
    calKeyPressed(event, data)
  elif data.mode == "Meet":
    meetKeyPressed(event,data)
      

def timerFired(data):
  if data.mode == "Home":
    homeTimerFired(data)
  elif data.mode == "Calendar":
    calTimerFired(data)
  elif data.mode == "Meet":
    meetTimerFired(data)
    
#Draw Do Not Disturb icon
def drawDisturb(canvas, data):
  if data.me.doNotDisturb:
      disturb = "N"
  else:
      disturb = "Y"
  cx = data.width - data.width / 10
  cy = data.width / 5
  canvas.create_text(cx, cy, text = disturb)
    
    
#Draw indicator for whether or not currently available      
def drawAvailable(canvas, data):
  if data.me.available:
      color = "green"
  else:
      color = "red"
  r = data.width / 25
  cx = data.width - data.width / 10 
  cy = data.width / 10
  canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill = color, outline = "goldenrod")

def redrawAll(canvas, data):
  canvas.create_text(4 * data.width / 5, data.height / 15, text = data.me.name, anchor = "e")
  #"Meet" drawn at top at all times
  canvas.create_text(data.width / 2, data.height / 15, text = "MEET", font = ("helvetica", 14, "bold"))
  #Draw availability and do not disturb indicators in top right
  drawAvailable(canvas, data)
  drawDisturb(canvas, data)
  margin = data.width / 10
  tabHeight = data.height - data.height / 8
  
  #Draw Calendar button
  c1 = margin
  c2 = data.width / 3 - margin
  calImageX = (data.width / 3) / 2
  calImageY = tabHeight + ((data.height - tabHeight) / 2)
  canvas.create_line(c1, tabHeight, c2, tabHeight)
  canvas.create_image(calImageX, calImageY, anchor="center", image=data.calImage)
    
  #Draw Home button
  h1 = data.width / 3 + margin
  h2 = data.width * 2 / 3 - margin
  homeImageX = (data.width / 3) + (data.width / 3) / 2
  homeImageY = tabHeight + (data.height - tabHeight) / 2
  canvas.create_line(h1, tabHeight, h2, tabHeight)
  canvas.create_image(homeImageX, homeImageY, anchor="center", image=data.homeImage)
  
  #Draw Meet Friends button
  f1 = data.width * 2 / 3 + margin
  f2 = data.width - margin
  meetImageX = data.width - ((data.width / 3) / 2)
  meetImageY = tabHeight + ((data.height - tabHeight) / 2)
  canvas.create_line(f1, tabHeight, f2, tabHeight)
  canvas.create_image(meetImageX, meetImageY, anchor="center", image=data.meetImage)



  
  ##MOVE to "Meet" mode only eventually
  # draw other players
  x = data.width / 2
  y = data.height / 2
  xName = data.width / 3
  for name in data.otherFriends:
    if data.otherFriends[name].doNotDisturb == True:
      disturb = "Y"
    else:
      disturb = "N"
    canvas.create_text(x, y, text = disturb, anchor = "center")
    canvas.create_text(xName, y, text = (data.otherFriends[name].name + ": "), anchor = "center")
    
  if data.mode == "Home":
    homeRedrawAll(canvas, data)
  elif data.mode == "Calendar":
    calRedrawAll(canvas, data)
  elif data.mode == "Meet":
    meetRedrawAll(canvas,data)
    
     
## HOME PAGE ##

def homeKeyPressed(event, data):
    pass
    
def homeMousePressed(event, data):
    pass
  
def homeTimerFired(data):
    pass

def homeRedrawAll(canvas, data):
    pass
    
## CALENDAR PAGE ##

def calKeyPressed(event, data):
  pass

def calMousePressed(event, data):
  pass
  
def calTimerFired(data):
  pass
  
def calRedrawAll(canvas, data):
  pass
  
## MEET PAGE ##

def meetKeyPressed(event, data):
  pass

def meetMousePressed(event, data):
  x,y = event.x, event.y
  
  margin = data.width / 10
  buttonMargin = data.height / 25
  tabHeight = data.height - data.height / 8
  bBottom = tabHeight - margin - buttonMargin - (data.height / 4)
  bHeight = data.height / 20
  if ((data.width / 2 + buttonMargin) < x < (data.width - buttonMargin - margin)) and (bBottom - bHeight < y < bBottom):
    resetRecommendData(data)
  
def meetTimerFired(data):
  if data.tabAnimate:
    if data.tabOpen:
      if data.successTabY < data.height / 11:
        data.successTabY += 5
      elif data.fadeSuccessTab > 9:
        #Fade for animation
        data.fadeSuccessTab -= 5
      else:
        data.tabOpen = False
    else:
    #Else, tab is in closing sequence animation
      data.tabTime += 1
      if data.tabTime > 55:
        if data.successTabY > 0:
          if data.fadeSuccessTab < 95:
            data.fadeSuccessTab += 8
          data.successTabY -= 3
        else:
          #Reset all pop-up tab values
          resetSuccessTabData(data)
  elif data.recommendAnimate:
    #Fade in prompt
    if data.fadeRecommendTab > 9:
      data.fadeRecommendTab -= 5
    

def meetRedrawAll(canvas, data):
  margin = data.width / 10
  tabHeight = data.height - data.height / 8
  canvas.create_rectangle(margin, data.height / 5, data.width - margin, tabHeight - margin)
  canvas.create_text(data.width / 2, data.height / 8, text = "'UP'")
  
  if data.tabAnimate:
    canvas.create_rectangle(2 * data.width / 3, 0, 5 * data.width / 6, data.successTabY, fill = "gray98", outline = "gray90")
    canvas.create_text((2 * data.width / 3) + (data.width / 12), data.height / 22, text = "Added!", anchor = "center", fill = "gray" + str(data.fadeSuccessTab), font = ("hervetica", 9))
    
  #Display prompt asking user for either time recommendation or cancel this  addition
  if data.recommendAnimate:
    #Button for scheduling "recommend"
    buttonMargin = data.height / 30
    bLeft = margin + buttonMargin
    bBottom = tabHeight - margin - buttonMargin - (data.height / 4)
    bWidth = data.width / 10
    bHeight = data.height / 20
    #Create general prompt
    canvas.create_rectangle(bLeft, (data.height / 5) + (3 * buttonMargin), data.width - margin - buttonMargin, tabHeight - (data.height / 3), fill = "gray98", outline = "gray" + str(data.fadeRecommendTab))
    canvas.create_text(data.width / 2, 4 * data.height / 11, text = "That time doesn't work out!\n We recommend " + data.recommendation + ".", anchor = "center", font = ("hervetica", 11))
    
    canvas.create_rectangle(bLeft + 10, bBottom - bHeight, (data.width / 2) - buttonMargin - 10, bBottom, fill = "gray98", outline = "gray" + str(data.fadeRecommendTab))
    canvas.create_text((bLeft + (data.width / 2 - buttonMargin)) / 2, bBottom - bHeight / 2, text = "Accept", fill = ("gray" + str(data.fadeRecommendTab)), anchor = "center", font = ("hervetica", 11, "bold"))
    
    #Button for scheduling "Cancel"
    #Currently not implemented (not active)
    bRight = data.width - margin - buttonMargin - 10
    canvas.create_rectangle(data.width / 2 + buttonMargin + 10, bBottom - bHeight, bRight - 10, bBottom, fill = "gray98", outline = "gray" + str(data.fadeRecommendTab))
    canvas.create_text(((data.width / 2 + buttonMargin) + bRight) / 2, bBottom - bHeight / 2, text = "Cancel", fill = ("gray" + str(data.fadeRecommendTab)), anchor = "center", font = ("hervetica", 11, "bold"))

  
####################################
# use the run function as-is 
####################################

def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Create root before calling init (so we can create images in init)
    root = Tk()
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 600)