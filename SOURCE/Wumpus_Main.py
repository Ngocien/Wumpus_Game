from tkinter import *
from tkinter import messagebox
import copy
import numpy as np
from data import *
from Objects import *

def handle_input():
    global lst
    global input_map
    global size

    if input_map == "random":
    	lst = random_Maze()
    	return

    UserInput ="..//DATA/" + input_map + ".txt"  #input("Enter input file: ")
    
    lst, size = get_maze(UserInput)

def display_score():
    global label_id
    C.delete(label_id)
    label_id = C.create_text(m*unit + 5*unit, n*unit/2, fill = "#f2ba0e", text = str(score), font=('Arial',20,'bold'))

def RunAlgorithm():
    print("Run")

def key_pressed(event):
	global p

	if event.keysym == "Escape":
		top.destroy()
		del p    
		Start(1, "map1")
	elif event.keysym == "Return": # Enter
		RunAlgorithm()
	else:
		p.key_move(event.keysym, C, n)
		top.update()

def Play():
    global top, C
    global Agent
    global unit, size
    global lst, ListAdjacency, ListWumpus, ListPit, ListStench, ListGold, ListBreeze
    global label_id, score
    top = Tk()
    unit = 25
    lst,ListAdjacency, ListWumpus, ListPit, ListStench, ListGold, ListBreeze = [],[],[],[],[],[],[]
    score = 0

    handle_input()

    top.title("WUMPUS GAME")
    C = Canvas(top, height = n*unit, width = m*unit + 10*unit, background = 'white')
    C.create_text(m*unit + 3*unit, n*unit/2 - 2*unit, fill = "#f61818", text = "S", font=('Arial',20,'bold'))
    C.create_text(m*unit + 4*unit, n*unit/2 - 2*unit, fill = "#1a98f6", text = "C", font=('Arial',20,'bold'))
    C.create_text(m*unit + 5*unit, n*unit/2 - 2*unit, fill = "#e3f00c", text = "O", font=('Arial',20,'bold'))
    C.create_text(m*unit + 6*unit, n*unit/2 - 2*unit, fill = "#1ce70a", text = "R", font=('Arial',20,'bold'))
    C.create_text(m*unit + 7*unit, n*unit/2 - 2*unit, fill = "#f2ba0e", text = "E", font=('Arial',20,'bold'))
    C.create_text(m*unit + 5*unit, n*unit/2 + 2*unit, fill = "white", text = "Press ENTER to play", font=('System', 10, 'bold'))
    C.create_text(m*unit + 5*unit, n*unit/2 + 3*unit, fill = "white", text = "Press ESC to return to menu", font=('System', 10, 'bold'))
    label_id = C.create_text(m*unit + 5*unit, n*unit/2, fill = "#f2ba0e", text = str(score), font=('Arial',20,'bold'))
    C.pack()

    ListAdjacency = scan_index(lst, size)

    top.bind("<Key>", key_pressed)
    top.mainloop()

def key_start(event):
	if event.keysym == "Return":
		menu.destroy()
		Play()

def Start(maze):
    global menu
    global input_map
    input_map = maze
    menu = Tk()
    menu.title("Menu")
    C = Canvas(menu, width = 100, height = 100)

    menu.bind("<Key>", key_start)
    C.pack()
    menu.mainloop()

Start("maze01")