from tkinter import *
import tkinter.font  as font
from PIL import ImageTk, Image, ImageOps
from matplotlib import pyplot as plt
from Data import *
from Objects import *

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
	Agent, ListWumpus, ListPit, ListBreeze, ListGold, ListBrick = scan_maze(lst, size,agent_mode)

def OpenRoom():
	global score, label_score
	global Agent
	
	index = Agent.index
	
	for i in range(len(ListBrick)):
		if ListBrick[i].index == index:
			ListBrick[i].destroy(C)
			ListBrick.pop(i)
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

	score -= 10
	display_score()
	Door.display(C)
	Agent.display(C)
	top.update()

	index = Agent.index
	dead = False
	#dead
	for w in ListWumpus:
		if w.index == index:
			w.display(C)
			dead = True
			break
	for p in ListPit:
		if p.index == index:
			p.display(C)
			dead = True
			break

	if dead:
		score -= 100
		display_score()
		top.update()
		time.sleep(1)
		Game_over()
		del Agent
		Menu("random")

def OpenAll():
	for br in ListBrick:
		br.destroy(C)
	for w in ListWumpus:
		w.display(C)
		for s in w.ListStench:
			if s.index < size*size: 
				s.display(C)
	for p in ListPit:
		p.display(C)
	for b in ListBreeze:
		b.display(C)
	for g in ListGold:
		g.display(C)

	Door.display(C)
	Agent.display(C)
	top.update()	

def Shoot():
	global score, wumpus
	score -= 100
	display_score()

	if Agent.status == "Right":
		index = Agent.index + size
	elif Agent.status == "Left":
		index = Agent.index - size
	elif Agent.status == "Up":
		index = Agent.index - 1
	else:
		index = Agent.index + 1

	Laser = laser(Agent.index // size, Agent.index % size)
	Laser.display(C, Agent.status)
	top.update()
	time.sleep(0.2)
	Laser.destroy(C)
	del Laser 
	
	for i in range(len(ListWumpus)):
		if ListWumpus[i].index == index:
			wumpus -= 1
			display_wumpus()
			ListWumpus[i].destroy(C)
			del ListWumpus[i]
			
			break

def CollectGold():
	global score, gold
	for i in range(len(ListGold)):
		if ListGold[i].index == Agent.index:
			ListGold[i].destroy(C)
			del ListGold[i]
			score += 100
			gold -= 1

			display_score()
			display_gold()
			break

def key_pressed(event):
	global Agent

	if game_mode == 'P':
		if event.keysym == "Escape":
			Game_over()
			del Agent
			Menu("random")

		elif event.keysym == "space":
			Shoot()
		elif event.keysym == "Return": # Enter
			CollectGold()
		else:
			pre_index = Agent.index
			Agent.key_move(event.keysym, C)
			if pre_index != Agent.index:
				OpenRoom()
				Agent.display(C)
				top.update()

	else: # Run mode
		if event.keysym == "Return":
			RunAlgorithm()

def btn_Play():
	menu.destroy()
	Play('P',agent_mode)

def btn_Run():
	menu.destroy()
	Play('R', agent_mode)

def btn_Shy():
	global agent_mode
	agent_mode = 'S'

def btn_Angry():
	global agent_mode
	agent_mode = 'A'

def key_Menu(event):
	if event.keysym == "Return":
		menu.destroy()
		Play('R', 'S')

def Menu(maze):
	global menu
	global input_map
	global agent_mode

	agent_mode ='S'
	input_map = maze
	unit = 50
	menu = Tk()
	menu.title("MENU WUMPUS")

	C = Canvas(menu,width= (size+5)*unit, height=size*unit, background='black')
	img = Image.open("../IMAGE/background.png")
	img = img.resize((unit*(size),unit*size), Image.ANTIALIAS)
	img = ImageTk.PhotoImage(img)
	C.create_image(0, 0, image = [img], anchor = 'nw')
	myfont = font.Font(size=20)
	button1 = Button(menu, text = "PLAY MODE",width=13,anchor = "center" , command = btn_Play, pady=10)
	button1['font'] = myfont
	button1.configure(activebackground = "#33B5E5", relief = GROOVE)
	button1.place(x = 490,y = 150)

	button2 = Button(menu, text = "RUN MODE", width=13,anchor = "center" , command = btn_Run, pady=10)
	button2['font'] = myfont
	button2.configure(activebackground = "#33B5E5", relief = GROOVE)
	button2.place(x = 490,y = 250)

	img3 = Image.open("../IMAGE/shy.png")
	img3 = img3.resize((unit*2,unit*2), Image.ANTIALIAS)
	img3 = ImageTk.PhotoImage(img3)

	button3 = Button(menu,image = img3, command= btn_Shy, border = 5 )
	button3.place(x = 490,y = 350)

	img4 = Image.open("../IMAGE/angry.png")
	img4 = img4.resize((unit*2+4,unit*2), Image.ANTIALIAS)
	img4 = ImageTk.PhotoImage(img4)

	button4 = Button(menu,image = img4, command= btn_Angry, border = 5 )
	button4.place(x = 490 + unit*2,y = 350)


	img1 = Image.open("../IMAGE/copyright.png")
	img1 = img1.resize((unit,unit), Image.ANTIALIAS)
	img1 = ImageTk.PhotoImage(img1)
	C.create_image(700,450 , image = [img1], anchor = 'nw')

	C.create_text((size-3)*unit + 3*unit, size*unit/2 - 3*unit, fill = 'Red', text = " W", font=('Arial',30,'bold'))
	C.create_text((size-3)*unit + 3.9*unit, size*unit/2 - 3*unit, fill = 'dark orange', text = "U", font=('Arial',30,'bold'))
	C.create_text((size-3)*unit + 4.7*unit, size*unit/2 - 3*unit, fill = 'yellow', text = "M", font=('Arial',30,'bold'))
	C.create_text((size-3)*unit + 5.4*unit, size*unit/2 - 3*unit, fill = 'lawn green', text = "P", font=('Arial',30,'bold'))
	C.create_text((size-3)*unit + 6.1*unit, size*unit/2 - 3*unit, fill = 'aqua', text = "U", font=('Arial',30,'bold'))
	C.create_text((size-3)*unit + 6.8*unit, size*unit/2 - 3*unit, fill = 'dark violet', text = "S", font=('Arial',30,'bold'))

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

	for i in range(11):
		C.create_line(0, i*unit, size*unit, i*unit)
		C.create_line(i*unit, 0, i*unit, size*unit) 

def display_score():
	global label_score
	C.delete(label_score)
	label_score = C.create_text( (size)*unit + 2.5*unit, size*unit/2 - 3.5*unit, fill = "skyblue3", text = str(score), font=('Times New Roman',80,'italic'))

def display_gold():
	global label_gold
	C.delete(label_gold)
	label_gold = C.create_text( (size)*unit + 4*unit, size*unit/2 - 1*unit, fill = "gold2", text = str(gold), font=('Arial',30))

def display_wumpus():
	global label_wumpus
	C.delete(label_wumpus)
	label_wumpus = C.create_text( (size)*unit + 4*unit, size*unit/2 - 2*unit, fill = "skyblue4", text = str(wumpus), font=('Arial',30))

def Game_over():
	global score
	score += 10
	display_score()

	OpenAll()
	time.sleep(2)
	top.destroy()

	global end, gold
	unit = 30
	size = 20
	end= Tk()
	end.title("GAME OVER")

	C = Canvas(end,width= size*unit, height=size*(unit-15), background='black')

	if Door.index == Agent.index  or gold == 0:
		C.create_text((size-10)*unit, size*unit/2 - 8*unit , fill = 'yellow', text = " CONGRATS ", font=('Arial',50,'bold'))
		
	else:
		C.create_text((size-10)*unit, size*unit/2 - 8*unit , fill = 'yellow', text = " GAME OVER ", font=('Arial',50,'bold'))
	label_score = C.create_text((size-10)*unit + 0.5*unit, size*unit/2 - 3*unit, fill = "hot pink", text = str(score), font=('Arial',80,'bold'))

	C.pack()
	end.mainloop()

def Play(m,a_mode):
	global top, C
	global Agent, Door
	global unit, size
	global lst, ListAdjacency, ListWumpus, ListPit, ListBreeze, ListGold, ListBrick
	global label_score, score
	global label_wumpus, wumpus
	global label_gold, gold
	global game_mode, agent_mode

	game_mode = m
	agent_mode = a_mode
	score = 0
	top = Tk()
	lst, ListAdjacency, ListWumpus, ListPit, ListBreeze, ListGold, ListBrick = [],[],[],[],[],[],[]
	score = 1000
	unit = 70
	handle_input()

	top.title("WUMPUS GAME")
	C = Canvas(top, height = (size)*unit, width = (size+5)*unit, background = '#d5dde0')

	img2 = Image.open("../IMAGE/score.png")
	img2 = img2.resize((unit*5,unit), Image.ANTIALIAS)
	img2 = ImageTk.PhotoImage(img2)
	C.create_image((size)*unit + 0.5*size, (size)*unit/2 - 5*unit, image = [img2], anchor = 'nw')

	label_score = C.create_text( (size)*unit + 2.5*unit, size*unit/2 - 3.5*unit, fill = "skyblue3", text = str(score), font=('Times New Roman',80,'italic'))

	wumpus = len(ListWumpus)
	gold = len(ListGold)

	img1 = Image.open("../IMAGE/wandg.png")
	img1 = img1.resize((unit,unit*2), Image.ANTIALIAS)
	img1 = ImageTk.PhotoImage(img1)
	C.create_image((size)*unit + 8.5*size, (size+2)*unit/2 - 3.5*unit, image = [img1], anchor = 'nw')

	label_wumpus = C.create_text( (size)*unit + 4*unit, size*unit/2 - 2*unit, fill = "skyblue4", text = str(wumpus), font=('Arial',30))
	label_gold = C.create_text( (size)*unit + 4*unit, size*unit/2 - 1*unit, fill = "gold2", text = str(gold), font=('Arial',30))

	img = Image.open("../IMAGE/control.png")
	img = img.resize((unit*(size-5),unit*(size-5)), Image.ANTIALIAS)
	img = ImageTk.PhotoImage(img)
	C.create_image(size*unit+0.5*size, (size+2)*unit/2 - 9*size , image = [img], anchor = 'nw')

	C.create_text((size*unit +2.5*unit, (size+2)*unit/2 + 3.5*unit), fill = 'burlywood4', text = '18127155_Vũ Công Minh - 18127046_Lư Ngọc Liên', font = ('Purisa',10))
	C.pack()

	draw_maze()
	Door = door(Agent.x, Agent.y)

	top.bind("<Key>", key_pressed)

	top.mainloop()

def generate_data(index):
	temp = ""
	for w in ListWumpus:
		for s in w.ListStench:
			if index == s.index :
				temp += "S"

	for b in ListBreeze:
		if index == b.index:
			temp += "B"

	for g in ListGold:
		if index == g.index:
			temp += "G"
	if temp == "":
		temp = "-"
	return temp

def RunAlgorithm():
	global top
	global Agent
	global lst
	global score

	init_index = Agent.init_room

	l = [(init_index, lst[init_index%size][init_index//size])]
	for a in ListAdjacency[init_index]:
		l.append(a[0]) 

	decision = Agent.action(l,C,top)

	while decision[2] != None:	# path
		goal = decision[2].pop(-1)
		decision[2].pop(0) # current_index
		for i in decision[2]:
			Agent.tile_move(i, C, top)
			OpenRoom()	
			top.update()
			time.sleep(0.2)

		if decision[1]: # Shoot
			Agent.facing_to(goal,C,top)
			Shoot()
			rq = Agent.Request_Update_Visited(goal)

			for r in rq:
				Agent.update_visited((r,generate_data(r), True))
				pre = []
				for adj in ListAdjacency[r]:
					pre.append(adj[0])
				Agent.update_predicted(r, pre)

		# go last tile
		Agent.tile_move(goal, C, top)
		OpenRoom()	
		top.update()
		time.sleep(0.2)

		l = [(Agent.index, generate_data(Agent.index))]
		for adj in ListAdjacency[Agent.index]:
			l.append(adj[0]) 

		decision = Agent.action(l, C, top)	

		if decision[0]:		# Tukkk
			CollectGold()

	path = Agent.ClimbOut(C)
	for i in path:
		Agent.tile_move(i,C,top)
		score -= 10
		display_score()
		top.update()
		time.sleep(0.2)

	time.sleep(2)
	Game_over()
	del Agent
	Menu("maze01")
