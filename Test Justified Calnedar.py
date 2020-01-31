# Basic Animation Framework
import calendar, datetime, math, string
from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    today = datetime.date.today()
    data.year = today.year
    data.day = today.day
    data.month = today.month
    data.weekDay = today.weekday()

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def redrawAll(canvas, data):
    color = "gray"
    x = data.width / 2
    y = data.height / 4
    
    #Text size is one 24th of board width
    textSize = 14 
    officialCal = str(calendar.month(data.year, data.month))
    officialCalFormatted = ""
    for line in officialCal.split("\n"):
        if line != "" and line != " ":
            newLine = justifyText(line, 50)
            officialCalFormatted += newLine + "\n"
            
    splitOfficial = officialCalFormatted.split("\n")
    a = "center"
    j = "left"
    for i in range(len(splitOfficial)):
        if i == 0:
            j = "center"
        elif i == 1:
            y += 10
        elif i == 2:
            j = "right"
        else:
            j = "left"
        splitOfficialLine = splitOfficial[i].strip()
        print(splitOfficialLine)
        canvas.create_text(x, y, text = splitOfficialLine, fill = color, justify = j, font = ("helvetica", textSize))
        print(j)
        #Space lines of calendar
        y += 20
   
## JUSTIFIED TEXT from 15112 week3, hw3, created by me (Andrew ID: justinw1) ##

def spaceCorrectly(t):
    newtext = ""
    for i in range(0, len(t)):
        if t[i] == "\n" or t[i] == "\t":
            if t[i + 1] == " " or ord(t[i + 1]) < 32:
                continue
            else: 
                c = " "
        elif t[i] == " ":
            if t[i + 1] == " " or ord(t[i + 1]) < 32:
                continue
            else: 
                c = " "
        #If there are no odd spaces or single spaces at that index, simply add word at index i
        else: 
            c = t[i]
        newtext += c
    return newtext.strip()
    
#Returns text with each line having a maximum of 30 characters
def breakLines(text, width):
    newtext = ""
    linelength = 0
    for word in text.split(" "):
        #The extra "+ 1" is always accounting for the index a space will take up - this linelength is used to determine if the width has been exceeded for that line
        if linelength + len(word) + 1 > width: 
            newtext += "\n"
            #Set of resetting actions to start a new line 
            linelength = 0
            linelength += len(word)
            newtext += word + " "
        else:
            linelength += len(word) + 1
            newtext+= word + " "
        
    return newtext[0 : len(newtext) - 1]
    
#Chooses base number of extra spaces needed to stretch out string
def howManySpaces(line, width):
    spacesNeeded = width - len(line)
    spacesCount = line.count(" ")
    if spacesCount == 0:
        return 0
    if spacesNeeded < spacesCount:
        return 1
    spaces = spacesNeeded // spacesCount
    #If there is an overlap of spacesCount to spacesNeeded, spaces must be at least one more in addition to calculated 'spaces'
    if spacesNeeded >= spacesCount:
        spaces += 1
    return spaces


#This extra checks to see how many extra spaces needed to be added in order to both evenly distribute them and meet the line width
def extraSpaces(line, width):
    spacesNeeded = width - len(line)
    spacesCount = line.count(" ")
    if spacesCount == 0:
        return 0
    extra = spacesNeeded % spacesCount
    #extra is 0 when the there is no "overlap" for spaces 
    return extra
    
#Determines number of blank spaces that need to be added at that specific point
def numBlanks(extra, spaces):
    if extra >= 1:
        extra = 1
    blanks = spaces + extra
    return blanks


#Ensures that each line is 30 characters long by adding appropriate number of spaces between words
def fixLineWidth(text, width):
    newtext = ""
    indents = 0
    
    #Divide and 'scan' the text by line
    for line in text.split("\n"):
        line = line.strip()
        spaces = howManySpaces(line, width)
        extra = extraSpaces(line, width)
        newLine = ""
        
        #If this is the last line of text, add line to newtext without justifying
        if indents == text.count("\n"):
            newtext += line.strip()
            break
        for word in line.split(" "): 
            if len(newLine) == width:
                break
            #If there is a space after the word, add a space in between this word and the next
            else:
                newLine += word + ((numBlanks(extra, spaces)) * " ") 
                #If there are more extra spaces to be used, subtract that amount
                if extra > 0:
                    extra -= 1
        #Once text has reached 30 characters, ensure there is no whitespace and wrap line
        indents += 1
        newtext += newLine.strip() + "\n"
    return newtext
            
#Returns final text by running each helper function to make specific modifications
def justifyText(text, width):
    text = spaceCorrectly(text)
    text = breakLines(text, width)
    text = fixLineWidth(text, width)
    return text

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
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

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)