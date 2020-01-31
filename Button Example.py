from tkinter import *

#Framework for button hovering taken from Eric Brunel, link below
#https://bytes.com/topic/python/answers/505848-tkinter-button-overrelief
root = Tk()

b = Button(root, width=8, text='foo')
b.pack()

def enterB(event):
   b.configure(text='bar')

def leaveB(event):
   b.configure(text='foo')

b.bind('<Enter>', enterB)
b.bind('<Leave>', leaveB)

root.mainloop()
