import calendar, datetime, math, string
from tkinter import *

##Profile and Calendar classes describe a user's specific characteristics

##########################
#Profile Class
##########################

#Describes each person's profile
class Profile(object):
    def __init__(self, name, disturb, calendar):
        self.name = name
        self.calendar = Calendar(calendar)
        self.doNotDisturb = disturb
        self.available = True

##########################
#Calendar Class
##########################
		
#Describes a schedule
class Calendar(object):
    #Store info about scheduled meetings as well as current date and time
    def __init__(self, schedule):
        today = datetime.date.today()
        self.year = today.year
        self.day = today.day
        self.month = today.month
        self.weekDay = today.weekday()
        #Test if calendar is file name or already formatted
        if isinstance(schedule, str):
            self.schedule = self.format(schedule)
        else:
            self.schedule = schedule
        self.meetSchedule = dict()
        
    #Create new blank schedule framework
    def newCalendar(self):
        dates = dict()
        days = str(calendar.month(self.year, self.month)).split()
        for date in days:
            #Test to see if item is a date for a month
            try:                                    
                date = int(date)
            except:                                                                 
                pass
            if isinstance(date, int) and 1 <= date <= 31:
                #Automatically set times for sleep 12-8AM
                temp = [("free", "sleep", 0, 8.5, "Sleep")] 
                dates[(str(self.month), str(date))] = temp
        return dates
        
    #Format marked calendar dates or times into a dictionary with 
    def format(self, schedule):
        dates = self.newCalendar()
        
        #Reads file and interprets information regarding event times
        with open("assets/" + schedule, "rt") as f:
            #Seperate event by line
            for line in f:
                line = line.strip()
                #Skip lines with comments or nothing
                if line == "" or line[0] == "#":
                    continue
                #In the format "month day priority starttime(h:mm) endtime message
                #Priority goes in Sleep (overrides others), school, work, eat, social, none
                line = line.split(" ")
                #Assume data is formatted properly
                if len(line) >= 5:
                    #This is adding a legitimate event
                    month = line[0]
                    day = line[1]
                    priority = line[2]
                    start = line[3]
                    #Format hr:min to decimal
                    start = start.split(":")
                    hr = int(start[0])
                    min = int(start[1]) / 60
                    startFormatted = hr + min
                    end = line[4]
                    end = end.split(":")
                    hr = int(end[0])
                    min = int(end[1]) / 60
                    endFormatted = hr + min
                    #Remaining words are part of message
                    msg = ""
                    for word in line[5:]:
                        msg += word
                        msg += " "
                    #Strip message of extra outer whitespace
                    msg = msg.strip()
                    temp = [("event",  priority, startFormatted, endFormatted, msg)]
                    if ((month,day) not in dates):
                        dates[(month,day)] = temp
                    else:
                        dates[(month,day)] += temp
                else:
                    #This is free time a person has marked -- msg is always None
                    month = line[0]
                    day = line[1]
                    priority = line[2]
                    start = line[3]
                    #Format hr:min to decimal
                    start = start.split(":")
                    hr = int(start[0])
                    min = int(start[1]) / 60
                    startFormatted = hr + min
                    end = line[4]
                    end = end.split(":")
                    hr = int(end[0])
                    min = int(end[1]) / 60
                    endFormatted = hr + min
                    temp = dict()
                    temp[("event",  priority, startFormatted, endFormatted)] = None
                    dates[(month, day)] = temp
        return dates
        
    #Add date to schedule
    def addMeeting(self, month, day, start, end, priority, msg, name):
        self.meetSchedule[(month, day)]= [(name, priority, start, end, msg)]
        
    #Draw Calendar formatted properly
    def drawCal(self, canvas, color, x, y):
        #Text size is one 24th of board width
        textSize = 14 
        officialCal = str(calendar.month(self.year, self.month))
        for i in range(len(officialCal)):
            c = officialCal[i]
            try:
                n = int(c)
            except:
                pass
        #Format this for better calendar
        canvas.create_text(x, y, text = officialCal, fill = color, anchor = \
        "center", justify = "center", font = ("helvetica", textSize))
        
    #Draw time
    def drawTime(self, canvas, x, y):
        t = datetime.datetime.now()
        if t.hour > 12:
            timeOfDay = "PM"
        else:
            timeOfDay = "AM"
        hour = str(t.hour % 12)
        if hour == "0":
            hour = "12"
        minute = t.minute 
        if minute < 10:
            minute = "0" + str(minute)
        else:
            minute = str(minute)
        #Text size is one 30th of board width
        textSize = 10
        #Format this for better calendar
        canvas.create_text(x, y, text = hour + ":" + minute + timeOfDay, \
        anchor = "center", justify = "center", font = ("helvetica", textSize))

        