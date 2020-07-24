import random, math, copy, string, ast, time
from tkinter import*
from image_util import*

## GENERAL FUNCTIONS (Applicable to animating in all three modes) ##

#Draw Do Not Disturb icon
def drawDisturb(canvas, data):
  if data.me.doNotDisturb:
      disturb = "Muted"
  else:
      disturb = "Online"
  cx = 5 * data.width / 6
  cy = data.height / 40
  canvas.create_text(cx, cy, text = disturb, anchor = "e", font = ("helvetica", 9, "italic"))
        
#Draw indicator for whether or not currently available      
def drawAvailable(canvas, data):
  if data.me.available:
      color = "DarkOliveGreen2"
  else:
      color = "red"
  r = data.width / 35
  cx = data.width - data.width / 10 
  cy = data.height / 40
  canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill = color, outline = "snow")
  
  
#Draws miniature button prompting user input
def drawButton(canvas, data):
    left = data.width / 4
    right = data.width * 3 / 4
    top = data.height / 5
    bottom = data.height * 2 / 5
    margin = data.height / 20
    canvas.create_rectangle(left, top, right, bottom, fill = "white")
    canvas.create_text(left, top + margin, text = "\t" + "Month: " + str(data.meetMonth), font = ("hervetica", 11), anchor = "w")
    canvas.create_text(left, top + margin * 2, text = "\t" + "Day: " + str(data.meetDate), font = ("hervetica", 11), anchor = "w")
    canvas.create_text(left, top + margin * 3, text = "\t" + "Start time: " + str(data.meetStart), font = ("hervetica", 11), anchor = "w")
    canvas.create_text(left, top + margin * 4, text = "\t" + "End time: " + str(data.meetEnd), font = ("hervetica", 11), anchor = "w")
    canvas.create_text(left, top + margin * 5, text = "\t" + "Priority: " + str(data.meetPriority), font = ("hervetica", 11), anchor = "w")
    canvas.create_text(left, top + margin * 6, text = "\t" + "Description: " + str(data.meetMsg), font = ("hervetica", 11), anchor = "w")

  
#Sends message asking for schedule
def addNewClient(data, name):
  msg = ""
  msg = "giveMeSchedule" + " " + name + "\n"
  if (msg != ""):
    print ("sending: ", msg)
    data.server.send(msg.encode())
  
#Sends user schedule to another
def sendSchedule(data, name):
  msg = ""
  schedule = str(data.me.calendar.schedule)
  schedule = schedule.replace(" ", "")
  msg = "saveThisSchedule" + " " + name + " " + schedule + " " + str(data.me.doNotDisturb) + "\n"
  if (msg != ""):
    print ("sending: ", msg)
    data.server.send(msg.encode())
    
#Resets all inputed data for meeting
def resetMeetData(data):
  data.scheduleCheckBox = False
  data.scheduleCheck = True
  data.meetName = ""
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
  data.msgType = False
  data.dateType = False
  data.startType = False
  data.endType = False
  data.monthType = True

#Reset all inputed data for recommendations
def resetRecommendData(data):
  data.recommendation = ""
  data.fadeRecommendTab = 99
  data.recommendAnimate = False
  
#Reset all inputed data for "Added!" tab animating
def resetSuccessTabData(data):
  data.tabOpen = True
  data.successTabY = 0
  data.fadeSuccessTab = 99
  data.tabTime = 0
  data.tabAnimate = False
  data.calMode = "cal"
    
    