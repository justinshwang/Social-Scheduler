#############################
# Sockets Client
#############################

import socket
import threading
from queue import Queue
from settings import SERVER_HOST, SERVER_PORT

def getHost(): 
  if SERVER_PORT != "":
    PORT = SERVER_PORT
  else:
    PORT = 80
  try: 
    if SERVER_HOST != "":
          return (SERVER_HOST, PORT)
    else:
      host_name = socket.gethostname() 
      host_ip = socket.gethostbyname(host_name) 
      print("Hostname :  ",host_name) 
      print("IP : ",host_ip) 
      return (host_ip, PORT)
  except: 
      print("Unable to retrieve Hostname/IP. Please enter in settings.")
      raise

HOST, PORT = getHost()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT)) # put IP address here or settings.py if playing on multiple computers
print("connected to server")

def handleServerMsg(server, serverMsg):     
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

# Barebones timer, mouse, and keyboard events

import random, math, copy, string, ast, time
from tkinter import*
from modules.image_util import*
from modules.Meet import*
from modules.ScheduleAlgorithms import*
from modules.GeneralAppFunctioning import*

####################################
# Function specific to Meet Application for Client operation
####################################

def init(data):
  name = input("Enter Name: ")
  update_calendar = input("Re-upload schedules? (y|n):")
  disturb = False
  data.me = Profile(name, disturb, update_calendar, HOST)
  data.otherFriends = dict()
  data.mode = "Home"
  data.optionsMode = "Closed"
  data.startingMessage = ""
  #Tab icons       
  data.meetImage = PhotoImage(file="assets/meet.gif")
  data.homeImage = PhotoImage(file="assets/home.gif")
  data.calImage = PhotoImage(file="assets/calendar.gif")
  
  #Calendar mode
  data.calMode = "cal"
  
  #Meet mode
  data.drawMeetButton = False
  # load data.xyz as appropriate
  data.scheduleCheckBox = False
  data.scheduleCheck = True
  data.meetMonth = ""
  data.meetDate = ""
  data.meetStart = ""
  data.meetEnd = ""
  data.meetStartFormatted = ""
  data.meetEndFormatted = ""
  data.meetPriorityFormatted = ""
  data.meetPriority = ""
  data.meetMsg = ""
  data.msg = ""
  data.warning = False
  
  data.monthType = True
  data.dateType = False
  data.startType = False
  data.endType = False
  data.priorityType = False
  data.msgType = False
  
  #Allows words to fade in or out, using list of colors
  data.fadeOriginal = 99
  data.fade = 99
  data.fadeTwo = 99
  
  #Success tab animation
  data.tabAnimate = False
  data.recommendAnimate = False
  data.tabOpen = True
  data.successTabY = 0
  data.fadeSuccessTab = 99
  data.fadeRecommendTab = 99
  data.tabTime = 0
  data.recommendation = ""
  data.failAnimate = False
  
## PRIMARY CONTROLLERS ##

def mousePressed(event, data):
  msg = ""
  x, y = event.x, event.y
  
  margin = data.width / 10
  diX = 5 * data.width / 6
  diY = data.height / 40
  tabHeight = data.height - data.height / 8
  if diX - margin <= x <= diX and 0 < y < 2 * diY:
    #If do not disturb button is pressed, change mode
    data.me.doNotDisturb = not data.me.doNotDisturb
    msg = "disturb %s\n" % data.me.name  
  elif 0 <= x < data.width / 3 and tabHeight <= y <= data.height:
    #If any of the modes are changed, also exit out of scheduling window, reset
    resetMeetData(data)
    resetSuccessTabData(data)
    resetRecommendData(data)
    #Change mode to calendar
    data.mode = "Calendar"
    #T fade color to white
    data.fade = data.fadeOriginal
    data.fadeTwo = data.fadeOriginal
  elif data.width / 3 <= x < 2 * data.width / 3 and tabHeight <= y <= data.height:
    resetMeetData(data)
    resetSuccessTabData(data)
    resetRecommendData(data)
    #Change mode to Home
    data.mode = "Home"
    data.fade = data.fadeOriginal
    data.fadeTwo = data.fadeOriginal
  elif data.width * 2 / 3 <= x <= data.width and tabHeight <= y <= data.height:
    resetMeetData(data)
    resetSuccessTabData(data)
    resetRecommendData(data)      
    #Change mode to Meet
    data.mode = "Meet"
    data.fade = data.fadeOriginal
    data.fadeTwo = data.fadeOriginal
  # send the message to other players!
  if (msg != ""):
    print ("sending: ", msg)
    data.server.send(msg.encode())
    
  if data.mode == "Home":
    homeMousePressed(event, data)
  elif data.mode == "Calendar":
    calMousePressed(event, data)
  elif data.mode == "Meet":
    meetMousePressed(event,data)
    
def keyPressed(event, data):
  if data.mode == "Home":
    homeKeyPressed(event, data)
  elif data.mode == "Calendar":
    calKeyPressed(event, data)
  elif data.mode == "Meet":
    meetKeyPressed(event,data)
      
def timerFired(data):
  #Fade animation pops each color from 
  if data.fade  > 9:
    data.fade -= 5
  if data.fade <= 30:
    if data.fadeTwo > 9:
      data.fadeTwo -= 5
    
  while (serverMsg.qsize() > 0):
    msg = serverMsg.get(False)
    try:
      print("received: ", msg, "\n")
      msg = msg.split()
      command = msg[0]
      
      if command == "disturb":
        name = msg[1]
        data.otherFriends[name].doNotDisturb = not data.otherFriends[name].doNotDisturb
      elif command == "newFriend":
        name = msg[1]
        addNewClient(data, name)
      elif command == "myIDis":
        pass
      elif command == "giveMeSchedule":
        name = msg[1]
        sendSchedule(data, name)
      elif command == "saveThisSchedule":
        name = msg[1]
        #Interprets string representation of dictionary
        schedule = ast.literal_eval(msg[3])
        if msg[3] == "True":
          disturb = True
        else:
          disturb = False
        #Create instance of Profile in friend with do not disturb defaulted to off or False
        data.otherFriends[name] = Profile(name, disturb, schedule, HOST)
      elif command == "success":
        fullMsg = msg[1]
        #Print this message 
      elif command == "update":
        name = msg[2]
        month = msg[3]
        date = msg[4]
        priority = msg[5]
        start = msg[6]
        end = msg[7]
        title = msg[8]
        for key in data.otherFriends[name].schedule:
          if key == (month, date):
            data.otherFriends[name].schedule[(month, date)].append(("event", priority, start, end, title))
    except:
      print("failed")
    serverMsg.task_done()
    
  if data.mode == "Home":
    homeTimerFired(data)
  elif data.mode == "Calendar":
    calTimerFired(data)
  elif data.mode == "Meet":
    meetTimerFired(data)

def redrawAll(canvas, data):
  #Background
  canvas.create_rectangle(0, 0, data.width, data.height, fill = "white", outline = "gray90")
  #Draw top bar
  canvas.create_rectangle(0, 0, data.width, (data.height / 20), fill = "gray98", outline = "gray98")
  canvas.create_line(0, data.height / 20, data.width, data.height / 20, fill = "gray95", width = 2)
  canvas.create_text(data.width / 10, data.height / 40, text = data.me.name, anchor = "w", font = ("helvetica", 11, "bold"))
  #"Meet" drawn at top at all times
  canvas.create_text(data.width / 2, (data.height / 13) + 10, text = "MEET", font = ("helvetica", 14, "bold"))
  #Draw availability and do not disturb indicators in top right
  drawAvailable(canvas, data)
  drawDisturb(canvas, data)
  #Draw time
  xTime = data.width / 2
  yTime = (data.height / 6) 
  data.me.calendar.drawTime(canvas, xTime, yTime)
  margin = data.width / 10
  tabHeight = data.height - data.height / 8
  
  #Create dividing line between tabs and rest of page
  canvas.create_rectangle(0, tabHeight, data.width, data.height, fill = "gray98", outline = "gray98")
  canvas.create_line(0, tabHeight, data.width, tabHeight, fill = "gray90")
  
  #Draw line seperating heading from main content
  left = margin
  top = data.height / 5
  right = data.width - margin
  canvas.create_line(left, top, right, top, width = 2)
  
  #Draw Calendar button
  c1 = margin
  c2 = data.width / 3 - margin
  calImageX = (data.width / 3) / 2
  calImageY = tabHeight + ((data.height - tabHeight) / 2)
  canvas.create_image(calImageX, calImageY, anchor="center", image=data.calImage)
    
  #Draw Home button
  h1 = data.width / 3 + margin
  h2 = data.width * 2 / 3 - margin
  homeImageX = (data.width / 3) + (data.width / 3) / 2
  homeImageY = tabHeight + ((data.height - tabHeight) / 2)
  canvas.create_image(homeImageX, homeImageY, anchor="center", image=data.homeImage)
  
  #Draw Meet Friends button
  f1 = data.width * 2 / 3 + margin
  f2 = data.width - margin
  meetImageX = data.width - ((data.width / 3) / 2)
  meetImageY = tabHeight + ((data.height - tabHeight) / 2)
  canvas.create_image(meetImageX, meetImageY, anchor="center", image=data.meetImage)
  
  if data.mode == "Home":
    canvas.create_line(h1, tabHeight + data.height / 9, h2, tabHeight + data.height / 9, width = 2)
    homeRedrawAll(canvas, data)
  elif data.mode == "Calendar":
    canvas.create_line(c1, tabHeight + data.height / 9, c2, tabHeight + data.height / 9, width = 2)
    calRedrawAll(canvas, data)
  elif data.mode == "Meet":
    canvas.create_line(f1, tabHeight + data.height / 9, f2, tabHeight + data.height / 9, width = 2)
    meetRedrawAll(canvas,data)
    
## HOME PAGE ##

def homeKeyPressed(event, data):
  pass
    
def homeMousePressed(event, data):
  pass
  
def homeTimerFired(data):
  pass

def homeRedrawAll(canvas, data):
  #Draw date heading
  date = "\"" + str(data.me.calendar.month) + "/" + str(data.me.calendar.day) + "/" + str(data.me.calendar.year) + "\""
  canvas.create_text(data.width / 2, (data.height / 9) + 12, text = str(date), fill = ("gray" + str(data.fade)), font = ("hervetica", 8, "bold"))
  
  #Draw current meetings
  margin = data.width / 10
  tabHeight = data.height - data.height / 8
  left = margin
  top = data.height / 5
  right = data.width - margin
  bottom = tabHeight - margin
  xName = left
  xIndicator = right
  count = 1
  
  #Draw recently added events with "*" next to it
  for key in (data.me.calendar.meetSchedule):
    month, date = key
    for i in range(len(data.me.calendar.meetSchedule[key])):
      type, priority, start, end, msg = data.me.calendar.meetSchedule[key][i]
      startHr = start // 1
      #Determine PM or AM
      if startHr < 12:
        startMeridiem = "AM"
      else:
        startMeridiem = "PM"
      startHr %= 12
      startHr = str(int(startHr))
      if startHr == "0":
        startHr = "12"
      startMin = int((start % 1) * 60)
      if startMin < 10:
        startMin = "0" + str(startMin)
      else:
        startMin = str(startMin)
      endHr = end // 1
      if endHr < 12:
        endMeridiem = "AM"
      else:
        endMeridiem = "PM"
      endHr %= 12
      endHr = str(int(endHr))
      if endHr == "0":
        endHr = "12"
      endMin = int((end % 1) * 60)
      if endMin < 10:
        endMin = "0" + str(endMin)
      else:
        endMin = str(endMin)
        
      indent = count * data.height / 20
      canvas.create_text(xIndicator, top + indent, text = msg, anchor = "e", fill = ("gray" + str(data.fadeTwo)), font = ("helvetica", 10, "italic"))
      canvas.create_text(xName, top + indent, text = "*" + startHr + ":" + startMin + startMeridiem + " - " + endHr + ":" + endMin + endMeridiem, justify = "left", fill = ("gray" + str(data.fadeTwo)), anchor = "w")
      canvas.create_text(data.width / 2, top + indent, text = type, justify = "center", fill = ("gray" + str(data.fadeTwo)), anchor = "center")
      count += 1
    
  #Draw today's events
  for key in (data.me.calendar.schedule):
    month, date = key
    for i in range(len(data.me.calendar.schedule[key])):
      type, priority, start,end, msg = data.me.calendar.schedule[key][i]
      name = data.me.name
      startHr = start // 1
      #Determine PM or AM
      if startHr < 12:
        startMeridiem = "AM"
      else:
        startMeridiem = "PM"
      startHr %= 12
      startHr = str(int(startHr))
      #Convert military time to 12 hour clock
      if startHr == "0" and startMeridiem == "AM":
        startHr = "12"
      startMin = int((start % 1) * 60)
      if startMin < 10:
        startMin = "0" + str(startMin)
      else:
        startMin = str(startMin)
      #Determine PM or AM
      endHr = end // 1
      if endHr < 12:
        endMeridiem = "AM"
      else:
        endMeridiem = "PM"
      endHr %= 12
      endHr = str(int(endHr))
      if endHr == "0" and endMeridiem == "AM":
        endHr = "12"
      endMin = int((end % 1) * 60)
      if endMin < 10:
        endMin = "0" + str(endMin)
      else:
        endMin = str(endMin)
      if str(data.me.calendar.month) == month and str(data.me.calendar.day) == date:
        indent = count * data.height / 20
        canvas.create_text(xIndicator, top + indent, text = str(msg), anchor = "e", fill = ("gray" + str(data.fadeTwo)), font = ("helvetica", 10, "italic"))
        canvas.create_text(xName, top + indent, text = startHr + ":" + startMin + startMeridiem + " - " + endHr + ":" + endMin + endMeridiem, justify = "left", fill = ("gray" + str(data.fadeTwo)), anchor = "w")
        canvas.create_text(data.width / 2, top + indent, text = name, justify = "center", fill = ("gray" + str(data.fadeTwo)), anchor = "center")
        
        count += 1
    
## CALENDAR PAGE ##

def calKeyPressed(event, data):
  #Take user input for scheduling
  if data.calMode == "add":
      data.warning = False
      command = event.keysym
      if command == "BackSpace" and data.msg != "":
          data.msg = data.msg[:(len(data.msg) - 1)]
      elif command == "Return":
          #Ensure a proper priority was given
          if data.msg in string.whitespace or data.msg == "":
            data.warning = True
          elif data.priorityType:
            p = set([None, "social", "eat", "work", "school", "sleep", \
            "Social", "Eat", "Work", "School", "Sleep"])
            if data.msg in p:
              data.scheduleCheck = False
            else:
              data.warning = True
          elif data.monthType:
            #Month is between 1 and 12 inclusive
            try: 
              num = int(data.msg)
              if 1 <= num <= 12:
                data.scheduleCheck = False
              else: data.warning = True
            except:
              data.warning = True
          elif data.dateType:
            #Day is between 1 and 31 inclusive
            try:
              num = int(data.msg)
              if 1 <= num <= 31:
                data.scheduleCheck = False
              else:
                data.warning = True
            except:
              data.warning = True
          elif data.startType or data.endType:
            #All times must have a colon
            if ":" not in data.msg:
              data.warning = True
            else:
              data.scheduleCheck = False
          else:
            #Entering "return" moves user onto next box
            data.scheduleCheck = False
      else:
          #Limit length of message
          if len(data.msg) <= 12:
              if (command in string.ascii_letters or command in \
              string.punctuation or command in string.digits):
                  data.msg += command
              elif command == "colon":
                  data.msg += ":"
              elif command == "space":
                  data.msg += " "
                  
def calMousePressed(event, data):
  x,y = event.x, event.y
  
  #Button locations for adding or deleting date
  margin = data.width / 10
  buttonMargin = data.height / 30
  tabHeight = data.height - data.height / 8
  bLeft = margin + buttonMargin
  bBottom = tabHeight - margin - buttonMargin
  bWidth = data.width / 10
  bHeight = data.height / 20
  bRight = data.width - margin - buttonMargin
  
  #Implement functionality for users to add new events in manually
  if data.calMode == "cal":
    if (bLeft < x < (data.width / 2) - buttonMargin) and (bBottom - bHeight < y < bBottom):
      #If "Add" button pressed
      data.calMode = "add"
    elif (data.width / 2 + buttonMargin) < x < bRight and (bBottom - bHeight < y < bBottom):
      #If "Clear" button pressed
      data.calMode = "clear"
      
  if data.calMode == "add":
    data.scheduleCheckBox = True
    if data.scheduleCheckBox == False:
      resetMeetData(data)
  if data.calMode == "clear":
    #Clear recently added and today's events
    for key in data.me.calendar.meetSchedule:
      data.me.calendar.meetSchedule[(key)] = ""
    for key in data.me.calendar.schedule:
      month, day = key
      if month == str(data.me.calendar.month) and day == str(data.me.calendar.day):
        data.me.calendar.schedule[key] = ""
    data.tabAnimate = True
    
  xRect = data.width / 6
  yRect = (data.height / 4)
  
  if data.scheduleCheckBox:
    #If user clicks outside of box, process of adding a meeting is cancelled
    if not xRect < x < xRect * 5 or not yRect < y < 5 * data.height / 6:
      #Reset all variables
      resetMeetData(data)
      
  
def calTimerFired(data):
  #Animate a roll down tab
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
          data.successTabY -= 4
        else:
          #Reset all pop-up tab values
          resetSuccessTabData(data)
  elif data.recommendAnimate:
    #Fade in prompt
    if data.fadeRecommendTab > 9:
      data.fadeRecommendTab -= 5
  
def calRedrawAll(canvas, data):
  #Draw calendar heading
  margin = data.width / 10
  tabHeight = data.height - data.height / 8
  color = "gray" + str(data.fadeTwo)
  data.me.calendar.drawCal(canvas, color, data.width / 2, (9 * data.height / 20))
  canvas.create_text(data.width / 2, (data.height / 9) + 12, text = "\"SCHEDULE\"", fill = "gray" + str(data.fade), font = ("hervetica", 8, "bold")) 
   
  #Button for scheduling "add"
  buttonMargin = data.height / 30
  bLeft = margin + buttonMargin
  bBottom = tabHeight - margin - buttonMargin
  bWidth = data.width / 10
  bHeight = data.height / 20
  canvas.create_rectangle(bLeft, bBottom - bHeight, (data.width / 2) - buttonMargin, bBottom, fill = "white")
  canvas.create_text((bLeft + (data.width / 2 - buttonMargin)) / 2, bBottom - bHeight / 2, text = "Add", fill = ("gray" + str(data.fade)), anchor = "center", font = ("hervetica", 11, "bold"))
  
  #Button for scheduling "Clear"
  bRight = data.width - margin - buttonMargin
  canvas.create_rectangle(data.width / 2 + buttonMargin, bBottom - bHeight, bRight, bBottom, fill = "white")
  canvas.create_text(((data.width / 2 + buttonMargin) + bRight) / 2, bBottom - bHeight / 2, text = "Clear", fill = ("gray" + str(data.fade)), anchor = "center", font = ("hervetica", 11, "bold"))
  
  if data.scheduleCheckBox:
    #Draw meet heading
    margin = data.width / 10
    tabHeight = data.height - data.height / 8

    #Sequence to taking user input display
  
    #Sequentially asks user for month, date, times, etc. in if/elif format
    if data.monthType:
        data.meetMonth = data.msg
        if data.scheduleCheck == False:
            data.monthType = False
            data.dateType = True
            data.msg = ""
            data.scheduleCheck = True
    elif data.dateType:
        data.meetDate = data.msg
        if data.scheduleCheck == False:
            data.dateType = False
            data.startType = True
            data.msg = ""
            data.scheduleCheck = True
    elif data.startType:
        data.meetStartFormatted = data.msg
        if data.scheduleCheck == False:
            data.startType = False
            data.endType = True
            time = data.meetStartFormatted
            time = time.split(":")
            hr = time[0]
            min = time[1]
            timeFormatted = float(hr) + float(int(min) / 60)
            data.meetStart = timeFormatted
            data.msg = ""
            data.scheduleCheck = True
    elif data.endType:
        data.meetEndFormatted = data.msg
        if data.scheduleCheck == False:
            data.endType = False
            data.priorityType = True
            time = data.meetEndFormatted
            time = time.split(":")
            hr = time[0]
            min = time[1]
            timeFormatted = float(hr) + float(int(min) / 60)
            data.meetEnd = timeFormatted
            data.msg = ""
            data.scheduleCheck = True
    elif data.priorityType:
        data.meetPriorityFormatted = data.msg
        if data.scheduleCheck == False:
            data.meetPriority = data.meetPriorityFormatted.lower()
            data.priorityType = False
            data.msgType = True
            data.msg = ""
            data.scheduleCheck = True
    elif data.msgType:
        data.meetMsg = data.msg
        if data.scheduleCheck == False:
            data.msg = ""
            data.msgType = False
            data.monthType = True
            #Do not ask for recommendations if this is called by calendar
            if data.calMode == "add":
                #Add meeting to user's schedule
                data.me.calendar.addMeeting(data.meetMonth, data.meetDate, \
                data.meetStart, data.meetEnd, data.meetPriority, data.meetMsg, \
                data.me.name)
                #Animate for success
                data.tabAnimate = True
            else:
              result, msg = recommendTime(data).split("*")
              if result == "success":
                #Add meeting to user's schedule
                data.me.calendar.addMeeting(data.meetMonth, data.meetDate, \
                data.meetStart, data.meetEnd, data.meetPriority, data.meetMsg, \
                data.meetName)
                #Animate for success
                data.tabAnimate = True
              else:
                data.failAnimate = True
                data.failMsg = msg
              #After data has been added, reset everything from input
            resetMeetData(data)
    
    #Draw Input boxes for user
    xRect = data.width / 6
    y = (data.height / 4)
    canvas.create_rectangle(xRect, y, 5 * data.width / 6, 5 * data.height / 6, fill = "gray99", outline = "gray90")
    margin = 50
    x =  data.width / 2
    mMY = y + margin
    mDY = y + 2 * margin
    tY =  y + 3 * margin
    t2Y = y + 4 * margin
    mPY = y + 5 * margin
    mMsgY = y + 6 * margin
    
    #Error message if inappropriate data entered
    if data.warning:
      canvas.create_text(xRect + 10, 5 * (data.height / 6) - 10, text = "Please enter a proper value", anchor = "w", font = ("hervetica", 7, "italic"))
      
    #Month
    smallBoxHeight = margin / 4
    smallBoxLen = 3 * data.width / 10
    lineColor = "black"
    if data.monthType:
      lineColor = "red4"
    canvas.create_rectangle(x, mMY - smallBoxHeight, x + smallBoxLen, mMY + smallBoxHeight, outline = lineColor)
    canvas.create_text(x + 5, mMY, text = data.meetMonth, anchor = "w", font = ("hervetica", 11))
    canvas.create_text(xRect + 8, mMY, text = "Enter Month: ", anchor = "w", font = ("hervetica", 8, "bold"))
    
    #Date
    lineColor = "black"
    if data.dateType:
      lineColor = "red4"
    canvas.create_rectangle(x, mDY - smallBoxHeight, x + smallBoxLen, mDY + smallBoxHeight, outline = lineColor)
    canvas.create_text(x + 5, mDY, text = data.meetDate, anchor = "w", font = ("hervetica", 11))
    canvas.create_text(xRect + 8, mDY, text = "Enter Date: ", anchor = "w", font = ("hervetica", 8, "bold"))
    
    #Start time
    lineColor = "black"
    if data.startType:
      lineColor = "red4"
    canvas.create_rectangle(x, tY - smallBoxHeight, x + smallBoxLen, tY + smallBoxHeight, outline = lineColor)
    canvas.create_text(x + 5, tY, text = data.meetStartFormatted, anchor = "w", font = ("hervetica", 11))
    #Caution when user enters "03" for example
    canvas.create_text(xRect + 8, tY, text = "Enter Start (h:mm): ", anchor = "w", font = ("hervetica", 8, "bold"))
    
    #End time
    lineColor = "black"
    if data.endType:
      lineColor = "red4"
    canvas.create_rectangle(x, t2Y - smallBoxHeight, x + smallBoxLen, t2Y + smallBoxHeight, outline = lineColor)
    canvas.create_text(x + 5, t2Y, text = data.meetEndFormatted, anchor = "w", font = ("hervetica", 11))
    canvas.create_text(xRect + 8, t2Y, text = "Enter End (h:mm): ", anchor = "w", font = ("hervetica", 8, "bold"))
    
    #Priority
    lineColor = "black"
    if data.priorityType:
      lineColor = "red4"
    canvas.create_rectangle(x, mPY - smallBoxHeight, x + smallBoxLen, mPY + smallBoxHeight, outline = lineColor)
    canvas.create_text(x + 5, mPY, text = data.meetPriorityFormatted, anchor = "w", font = ("hervetica", 11))
    canvas.create_text(xRect + 8, mPY, text = "Enter Priority: ", anchor = "w", font = ("hervetica", 8, "bold"))
    
    #Title
    lineColor = "black"
    if data.msgType:
      lineColor = "red4"
    canvas.create_rectangle(x, mMsgY - smallBoxHeight, x + smallBoxLen, mMsgY + smallBoxHeight, outline = lineColor)
    canvas.create_text(x + 5, mMsgY, text = data.meetMsg, anchor = "w", font = ("hervetica", 11))
    canvas.create_text(xRect + 8, mMsgY, text = "Enter Title: ", anchor = "w", font = ("hervetica", 8, "bold"))
  
  #Draws animation for pop-up tab
  if data.tabAnimate:
    message = "Added!"
    #Change message if "clear" button was pressed 
    if data.calMode == "clear":
      message = "Cleared!"
    canvas.create_rectangle(2 * data.width / 3, 0, 5 * data.width / 6, data.successTabY, fill = "gray98", outline = "aquamarine", width = 2)
    canvas.create_text((2 * data.width / 3) + (data.width / 12), data.height / 22, text = message, anchor = "center", justify = "center", fill = "gray" + str(data.fadeSuccessTab), font = ("hervetica", 8))
  
## MEET PAGE ##

def meetKeyPressed(event, data):
  #Take user input for scheduling
  if data.scheduleCheck and data.calMode != "add":
      data.warning = False
      command = event.keysym
      if command == "BackSpace" and data.msg != "":
          data.msg = data.msg[:(len(data.msg) - 1)]
      elif command == "Return":
          #Ensure a proper priority was given
          if data.msg in string.whitespace or data.msg == "":
            data.warning = True
          elif data.priorityType:
            p = set(["none", "social", "eat", "work", "school", "sleep", \
            "Social", "Eat", "Work", "School", "Sleep"])
            if data.msg in p:
              data.scheduleCheck = False
            else:
              data.warning = True
          elif data.monthType:
            #Month is between 1 and 12 inclusive
            try: 
              num = int(data.msg)
              if 1 <= num <= 12:
                data.scheduleCheck = False
              else: data.warning = True
            except:
              data.warning = True
          elif data.dateType:
            #Day is between 1 and 31 inclusive
            try:
              num = int(data.msg)
              if 1 <= num <= 31:
                data.scheduleCheck = False
              else:
                data.warning = True
            except:
              data.warning = True
          elif data.startType or data.endType:
            #All times must have a colon
            if ":" not in data.msg:
              data.warning = True
            else:
              data.scheduleCheck = False
          else:
            #Entering "return" moves user onto next box
            data.scheduleCheck = False
      else:
          #Limit length of message
          if len(data.msg) <= 12:
              if (command in string.ascii_letters or command in \
              string.punctuation or command in string.digits):
                  data.msg += command
              elif command == "colon":
                  data.msg += ":"
              elif command == "space":
                  data.msg += " "

def meetMousePressed(event, data):
  x, y = event.x, event.y
  #If user clicks line of that friend, ask for a date, times, priority 
  #(or None as default), and description
  indent = data.height / 20
  top = data.height / 5
  margin = data.width / 10
  
  xRect = data.width / 6
  yRect = (data.height / 4)
  
  if data.scheduleCheckBox:
    #If user clicks outside of box, process of adding a meeting is cancelled
    if not xRect < x < xRect * 5 or not yRect < y < 5 * data.height / 6:
      #Reset all variables
      resetMeetData(data)
  
  if len(data.otherFriends) > 0:
    if (margin < x < data.width - margin) and y > top:
      if (y - top) // indent < len(data.otherFriends):
        friendNum = int((y - top) // indent)  
        count = 0
        for name in data.otherFriends:
          if count == friendNum:
            friend = name
            data.meetName = friend
            #Initiate sequence to ask user to input information
            data.scheduleCheckBox = True
            break
          count += 1
  
  #Checks if Cancel or Accept button was pressed
  if data.recommendAnimate:
    margin = data.width / 10
    buttonMargin = data.height / 30
    bRight = data.width - margin - buttonMargin - 10
    bLeft = margin + buttonMargin
    tabHeight = data.height - data.height / 8
    bBottom = tabHeight - margin - buttonMargin - (data.height / 4)
    bHeight = data.height / 20
    
    #If cancel pressed
    if ((data.width / 2 + buttonMargin) + 10 < x < bRight - 10) and (bBottom - bHeight < y < bBottom):
      resetRecommendData(data)
      resetMeetData(data)
    elif bLeft + 10 < x <  (data.width / 2) - buttonMargin - 10 and bBottom - bHeight < y < bBottom:
      #Add meeting to schedule if "Accept" button pressed
      data.me.calendar.addMeeting(data.meetMonth, data.meetDate, \
      data.meetStart, data.meetEnd, data.meetPriority, data.meetMsg, \
      data.meetName)
      #Animate for success
      data.tabAnimate = True
      resetRecommendData(data)
      resetMeetData(data)
          
      
def meetTimerFired(data):
  #Animate a roll down tab
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
  elif data.failAnimate:
    if data.tabTime < 75:
      data.tabTime += 1
    else:
      data.failAnimate = False
  
  
def meetRedrawAll(canvas, data):
  #Draw meet heading
  margin = data.width / 10
  tabHeight = data.height - data.height / 8
  left = margin
  top = data.height / 5
  right = data.width - margin
  canvas.create_text(data.width / 2, (data.height / 9) + 12, text = "\"UP\"", fill = "gray" + str(data.fade), font = ("hervetica", 8, "bold"))

  #Draw friends' current availabilities
  xName = left
  xIndicator = right
  #Count used to track indentation amount
  count = 1
  for name in data.otherFriends:
    if data.otherFriends[name].doNotDisturb:
      disturb = "Muted"
    else:
      disturb = "Online"
    indent = count * data.height / 20
    canvas.create_text(xIndicator, top + indent, text = disturb + "\t", anchor = "e", justify = "left", fill = ("gray" + str(data.fadeTwo)), font = ("helvetica", 10, "italic"))
    canvas.create_text(xName, top + indent, text = "\t" + (data.otherFriends[name].name + ": "), fill = ("gray" + str(data.fadeTwo)), anchor = "w")
    count += 1

  if data.scheduleCheckBox and data.calMode != "add":
    #Draw Input boxes for user
    xRect = data.width / 6
    y = (data.height / 4)
    canvas.create_rectangle(xRect, y, 5 * data.width / 6, 5 * data.height / 6, fill = "gray99", outline = "gray90")
    margin = 50
    x =  data.width / 2
    mMY = y + margin
    mDY = y + 2 * margin
    tY =  y + 3 * margin
    t2Y = y + 4 * margin
    mPY = y + 5 * margin
    mMsgY = y + 6 * margin
      
  
    #Sequentially asks user for month, date, times, etc. in if/elif format
    if data.monthType:
        data.meetMonth = data.msg
        if data.scheduleCheck == False:
            data.monthType = False
            data.dateType = True
            data.msg = ""
            data.scheduleCheck = True
    elif data.dateType:
        data.meetDate = data.msg
        if data.scheduleCheck == False:
            data.dateType = False
            data.startType = True
            data.msg = ""
            data.scheduleCheck = True
    elif data.startType:
        data.meetStartFormatted = data.msg
        if data.scheduleCheck == False:
            data.startType = False
            data.endType = True
            time = data.meetStartFormatted
            time = time.split(":")
            hr = time[0]
            min = time[1]
            timeFormatted = float(hr) + float(int(min) / 60)
            data.meetStart = timeFormatted
            data.msg = ""
            data.scheduleCheck = True
    elif data.endType:
        data.meetEndFormatted = data.msg
        if data.scheduleCheck == False:
            data.endType = False
            data.priorityType = True
            time = data.meetEndFormatted
            time = time.split(":")
            hr = time[0]
            min = time[1]
            timeFormatted = float(hr) + float(int(min) / 60)
            data.meetEnd = timeFormatted
            data.msg = ""
            data.scheduleCheck = True
    elif data.priorityType:
        data.meetPriorityFormatted = data.msg
        if data.scheduleCheck == False:
            data.meetPriority = data.meetPriorityFormatted.lower()
            data.priorityType = False
            data.msgType = True
            data.msg = ""
            data.scheduleCheck = True
    elif data.msgType:
        data.meetMsg = data.msg
        if data.scheduleCheck == False:
            data.msg = ""
            data.msgType = False
            data.monthType = True
            #Do not ask for recommendations if this is called by calendar
            if data.calMode == "add":
                #Add meeting to user's schedule
                data.me.calendar.addMeeting(data.meetMonth, data.meetDate, \
                data.meetStart, data.meetEnd, data.meetPriority, data.meetMsg, \
                data.me.name)
                #Animate for success
                data.tabAnimate = True
            else:
              result, msg = recommendTime(data).split("*")
              if result == "success":
                #Add meeting to user's schedule
                data.me.calendar.addMeeting(data.meetMonth, data.meetDate, \
                data.meetStart, data.meetEnd, data.meetPriority, data.meetMsg, \
                data.meetName)
                #Animate for success
                data.tabAnimate = True
                resetMeetData(data)
              elif result == "impossible":
                data.failAnimate = True
                data.failMsg = msg
                resetMeetData(data)
              else:
                #Recommend other times
                recommendation = msg
                hr = float(msg) // 1
                min = int((float(msg) % 1) * 60)
                if min < 10:
                  minFormatted = "0" + str(min)
                else:
                  minFormatted = str(min)
                data.recommendation = str(int(hr)) + ":" + minFormatted
                data.recommendAnimate = True
         
           
    #Error message if inappropriate data entered
    if data.warning:
      canvas.create_text(xRect + 10, 5 * (data.height / 6) - 10, text = "Please enter a proper value", anchor = "w", font = ("hervetica", 7, "italic"))
      
    #Month
    smallBoxHeight = margin / 4
    smallBoxLen = 3 * data.width / 10
    lineColor = "black"
    if data.monthType:
      lineColor = "red4"
    canvas.create_rectangle(x, mMY - smallBoxHeight, x + smallBoxLen, mMY + smallBoxHeight, outline = lineColor)
    canvas.create_text(x + 5, mMY, text = data.meetMonth, anchor = "w", font = ("hervetica", 11))
    canvas.create_text(xRect + 8, mMY, text = "Enter Month: ", anchor = "w", font = ("hervetica", 8, "bold"))
    
    #Date
    lineColor = "black"
    if data.dateType:
      lineColor = "red4"
    canvas.create_rectangle(x, mDY - smallBoxHeight, x + smallBoxLen, mDY + smallBoxHeight, outline = lineColor)
    canvas.create_text(x + 5, mDY, text = data.meetDate, anchor = "w", font = ("hervetica", 11))
    canvas.create_text(xRect + 8, mDY, text = "Enter Date: ", anchor = "w", font = ("hervetica", 8, "bold"))
    
    #Start time
    lineColor = "black"
    if data.startType:
      lineColor = "red4"
    canvas.create_rectangle(x, tY - smallBoxHeight, x + smallBoxLen, tY + smallBoxHeight, outline = lineColor)
    canvas.create_text(x + 5, tY, text = data.meetStartFormatted, anchor = "w", font = ("hervetica", 11))
    #Caution when user enters "03" for example
    canvas.create_text(xRect + 8, tY, text = "Enter Start (h:mm): ", anchor = "w", font = ("hervetica", 8, "bold"))
    
    #End time
    lineColor = "black"
    if data.endType:
      lineColor = "red4"
    canvas.create_rectangle(x, t2Y - smallBoxHeight, x + smallBoxLen, t2Y + smallBoxHeight, outline = lineColor)
    canvas.create_text(x + 5, t2Y, text = data.meetEndFormatted, anchor = "w", font = ("hervetica", 11))
    canvas.create_text(xRect + 8, t2Y, text = "Enter End (h:mm): ", anchor = "w", font = ("hervetica", 8, "bold"))
    
    #Priority
    lineColor = "black"
    if data.priorityType:
      lineColor = "red4"
    canvas.create_rectangle(x, mPY - smallBoxHeight, x + smallBoxLen, mPY + smallBoxHeight, outline = lineColor)
    canvas.create_text(x + 5, mPY, text = data.meetPriorityFormatted, anchor = "w", font = ("hervetica", 11))
    canvas.create_text(xRect + 8, mPY, text = "Enter Priority: ", anchor = "w", font = ("hervetica", 8, "bold"))
    
    #Title
    lineColor = "black"
    if data.msgType:
      lineColor = "red4"
    canvas.create_rectangle(x, mMsgY - smallBoxHeight, x + smallBoxLen, mMsgY + smallBoxHeight, outline = lineColor)
    canvas.create_text(x + 5, mMsgY, text = data.meetMsg, anchor = "w", font = ("hervetica", 11))
    canvas.create_text(xRect + 8, mMsgY, text = "Enter Title: ", anchor = "w", font = ("hervetica", 8, "bold"))
    
  #Button for scheduling "recommend"
  buttonMargin = data.height / 30
  bLeft = margin + buttonMargin
  bBottom = tabHeight - margin - buttonMargin - (data.height / 4)
  bWidth = data.width / 10
  bHeight = data.height / 20
      
  if data.tabAnimate:
    message = "Added!"
    canvas.create_rectangle(2 * data.width / 3, 0, 5 * data.width / 6, data.successTabY, fill = "gray98", outline = "aquamarine")
    canvas.create_text((2 * data.width / 3) + (data.width / 12), data.height / 22, text = message, anchor = "center", justify = "center", fill = "gray" + str(data.fadeSuccessTab), width = 3, font = ("hervetica", 9))
  #Display prompt asking user for either time recommendation or cancel this  addition
  if data.recommendAnimate:
    
    #Create general prompt
    canvas.create_rectangle(bLeft, (data.height / 5) + (3 * buttonMargin), data.width - margin - buttonMargin, tabHeight - (data.height / 3), fill = "gray98", outline = "gray" + str(data.fadeRecommendTab))
    canvas.create_text(data.width / 2, 4 * data.height / 11, text = "\n We recommend " + data.recommendation + ".", anchor = "center", justify = "center", font = ("hervetica", 11, "bold"))
    
    #Button for "Accept" recommendation
    canvas.create_rectangle(bLeft + 10, bBottom - bHeight, (data.width / 2) - buttonMargin - 10, bBottom, fill = "gray98", outline = "gray" + str(data.fadeRecommendTab))
    canvas.create_text((bLeft + (data.width / 2 - buttonMargin)) / 2, bBottom - bHeight / 2, text = "Accept", fill = ("gray" + str(data.fadeRecommendTab)), anchor = "center", font = ("hervetica", 11, "bold"))
    
    #Button for scheduling "Cancel"
    #Currently not implemented (not active)
    bRight = data.width - margin - buttonMargin - 10
    canvas.create_rectangle(data.width / 2 + buttonMargin + 10, bBottom - bHeight, bRight - 10, bBottom, fill = "gray98", outline = "gray" + str(data.fadeRecommendTab))
    canvas.create_text(((data.width / 2 + buttonMargin) + bRight) / 2, bBottom - bHeight / 2, text = "Cancel", fill = ("gray" + str(data.fadeRecommendTab)), anchor = "center", font = ("hervetica", 11, "bold"))
    
  if data.failAnimate:
    canvas.create_rectangle(bLeft, (data.height / 5) + (3 * buttonMargin), data.width - margin - buttonMargin, tabHeight - (data.height / 3), fill = "gray98", outline = "gray90", width = 3)
    canvas.create_text(data.width / 2, 4 * data.height / 11, text = data.failMsg, anchor = "center", font = ("hervetica", 11, "bold"))

####################################
#         run function             #
####################################

def run(width, height, serverMsg = None, server = None):
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
    data.server = server
    data.serverMsg = serverMsg
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

serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

run(400, 600, serverMsg, server)