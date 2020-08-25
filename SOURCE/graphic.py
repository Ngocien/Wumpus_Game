from tkinter import *
import tkinter.font  as font
from data import *
from Objects import *
import tkinter
unit = 50
maze , size = get_maze("../DATA/maze01.txt")

top =  Tk()
top.title("MENU WUMPUS")

C = Canvas(top,width= (size+5)*unit, height=size*unit, background='black')
img = Image.open("../IMAGE/background.png")
img = img.resize((unit*(size),unit*size), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
C.create_image(0, 0, image = img, anchor = 'nw')

def play():
    print("hello")
def credit():
    print("credit")
def Exit():
    print("exit")
myfont = font.Font(size=20)
button1 = Button(top, text = "PLAY",width=10,anchor = "center" , command = play, pady=8)
button1['font'] = myfont
button1.configure(activebackground = "#33B5E5", relief = GROOVE)
button1.place(x = 500,y = 150)

button2 = Button(top, text = "CREDIT", width=10,anchor = "center" , command = credit, pady=8)
button2['font'] = myfont
button2.configure(activebackground = "#33B5E5", relief = GROOVE)
button2.place(x = 500,y = 250)

button3 = Button(top, text = "EXIT",width=10,anchor = "center"  , command = Exit, pady=8)
button3['font'] = myfont
button3.configure(activebackground = "#33B5E5", relief = GROOVE)
button3.place(x = 500,y = 350)


C.create_text((size-4)*unit + 3*unit, size*unit/2 - 3*unit, fill = 'Red', text = " W", font=('Arial',30,'bold'))
C.create_text((size-4)*unit + 4*unit, size*unit/2 - 3*unit, fill = 'dark orange', text = "U", font=('Arial',30,'bold'))
C.create_text((size-4)*unit + 5*unit, size*unit/2 - 3*unit, fill = 'yellow', text = "M", font=('Arial',30,'bold'))
C.create_text((size-4)*unit + 6*unit, size*unit/2 - 3*unit, fill = 'lawn green', text = "P", font=('Arial',30,'bold'))
C.create_text((size-4)*unit + 7*unit, size*unit/2 - 3*unit, fill = 'aqua', text = "U", font=('Arial',30,'bold'))
C.create_text((size-4)*unit + 8*unit, size*unit/2 - 3*unit, fill = 'dark violet', text = "S", font=('Arial',30,'bold'))





C.pack()
top.mainloop()






