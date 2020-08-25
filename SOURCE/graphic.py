from tkinter import *
import tkinter.font  as font
from PIL import ImageTk, Image, ImageOps
from Data import *
from Objects import *
unit = 50
maze , size = get_maze("../DATA/maze01.txt")

def handle_input():
	global input_map
	global Agent
	global unit, size
	global lst, ListAdjacency, ListWumpus, ListPit, ListBreeze, ListGold, ListBrick

	if input_map == "random":
		lst, size = random_Maze()
	else:
		UserInput ="..//DATA/" + input_map + ".txt"  #input("Enter input file: ")
		lst, size = get_maze(UserInput)

	ListAdjacency = scan_index(lst,size)
	Agent, ListWumpus, ListPit, ListBreeze, ListGold, ListBrick = scan_maze(lst, size)

def OpenRoom():
	index = Agent.index
	
	for br in ListBrick:
		if br.index == index:
			br.destroy(C)
			break
	for w in ListWumpus:
		if w.index == index:
			w.display(C)
			break
	for p in ListPit:
		if p.index == index:
			p.display(C)
			break
	for b in ListBreeze:
		if b.index == index:
			b.display(C)
			break
	for w in ListWumpus:
		if w.find_stench(index, C):
			break
	for g in ListGold:
		if g.index == index:
			g.display(C)
			break

	Agent.display(C)

def OpenAll():
	for br in ListBrick:
		br.destroy(C)
	for w in ListWumpus:
		w.display(C)
	for p in ListPit:
		p.display(C)
	for b in ListBreeze:
		b.display(C)
	for g in ListGold:
		g.display(C)

	Agent.display(C)
	top.update()	

def Shoot():
	print("Chíu Chíu")
	if Agent.status == "Right":
		index = Agent.index + size
	elif Agent.status == "Left":
		index = Agent.index - size
	elif Agent.status == "Up":
		index = Agent.index - 1
	else:
		index = Agent.index + 1

	for i in range(len(ListWumpus)):
		if ListWumpus[i].index == index:
			ListWumpus[i].destroy(C)
			del ListWumpus[i]
			break

def CollectGold():
	for i in range(len(ListGold)):
		if ListGold[i].index == Agent.index:
			ListGold[i].destroy(C)
			del ListGold[i]
			break

def key_pressed(event):
	global Agent

	if event.keysym == "Escape":
		OpenAll()
		time.sleep(5)
		top.destroy()
		del Agent
		Menu("maze01")
	elif event.keysym == "space":
		Shoot()
		OpenRoom()
	elif event.keysym == "Return": # Enter
		CollectGold()
	else:
		Agent.key_move(event.keysym, C)
		OpenRoom()
		top.update()

def credit():
    print("credit")
def Exit():
    print("exit")

def Play():
    global top, C
    global Agent
    global unit, size
    global lst, ListAdjacency, ListWumpus, ListPit, ListBreeze, ListGold, ListBrick
    global label_id, score
    top = Tk()
    lst, ListAdjacency, ListWumpus, ListPit, ListBreeze, ListGold, ListBrick = [],[],[],[],[],[],[]
    score = 0
    unit = 70
    handle_input()

    top.title("WUMPUS GAME")
    C = Canvas(top, height = size*unit, width = size*unit, background = 'light gray')

    C.pack()

    draw_maze()


    top.bind("<Key>", key_pressed)
    top.mainloop()

def btn_Play():
	menu.destroy()
	Play()

def key_Menu(event):
	if event.keysym == "Return":
		menu.destroy()
		Play()

def Menu(maze):
	global menu
	global input_map
	input_map = maze

	menu = Tk()
	menu.title("MENU WUMPUS")

	C = Canvas(menu,width= (size+5)*unit, height=size*unit, background='black')
	img = Image.open("../IMAGE/background.png")
	img = img.resize((unit*(size),unit*size), Image.ANTIALIAS)
	img = ImageTk.PhotoImage(img)
	C.create_image(0, 0, image = img, anchor = 'nw')

	myfont = font.Font(size=20)
	button1 = Button(menu, text = "PLAY",width=10,anchor = "center" , command = btn_Play, pady=8)
	button1['font'] = myfont
	button1.configure(activebackground = "#33B5E5", relief = GROOVE)
	button1.place(x = 500,y = 150)

	button2 = Button(menu, text = "CREDIT", width=10,anchor = "center" , command = credit, pady=8)
	button2['font'] = myfont
	button2.configure(activebackground = "#33B5E5", relief = GROOVE)
	button2.place(x = 500,y = 250)

	button3 = Button(menu, text = "EXIT",width=10,anchor = "center"  , command = Exit, pady=8)
	button3['font'] = myfont
	button3.configure(activebackground = "#33B5E5", relief = GROOVE)
	button3.place(x = 500,y = 350)

	C.create_text((size-4)*unit + 3*unit, size*unit/2 - 3*unit, fill = 'Red', text = " W", font=('Arial',30,'bold'))
	C.create_text((size-4)*unit + 4*unit, size*unit/2 - 3*unit, fill = 'dark orange', text = "U", font=('Arial',30,'bold'))
	C.create_text((size-4)*unit + 5*unit, size*unit/2 - 3*unit, fill = 'yellow', text = "M", font=('Arial',30,'bold'))
	C.create_text((size-4)*unit + 6*unit, size*unit/2 - 3*unit, fill = 'lawn green', text = "P", font=('Arial',30,'bold'))
	C.create_text((size-4)*unit + 7*unit, size*unit/2 - 3*unit, fill = 'aqua', text = "U", font=('Arial',30,'bold'))
	C.create_text((size-4)*unit + 8*unit, size*unit/2 - 3*unit, fill = 'dark violet', text = "S", font=('Arial',30,'bold'))

	menu.bind("<Key>", key_Menu)
	C.pack()
	menu.mainloop()

def draw_maze():
	global Agent
	global ListWumpus, ListPit, ListBreeze, ListGold, ListBrick
	global C

	Agent.display(C)

	for br in ListBrick:
		br.display(C)
		if br.index == Agent.index:
			br.destroy(C)

	for i in range(10):
		C.create_line(0, i*unit, size*unit, i*unit)
		C.create_line(i*unit, 0, i*unit, size*unit) 