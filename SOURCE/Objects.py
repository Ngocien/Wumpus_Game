from PIL import ImageTk, Image, ImageOps
import time, random
from Algorithm import *
unit = 70
size = 10
# Agent object
class Agent(object):
    def __init__(self, imgpath_down, imgpath_up, imgpath_right, x, y,mode):
        temp = Image.open(imgpath_down) 
        img_down = temp.resize((50, 50), Image.ANTIALIAS)
        self.down = img_down

        temp1 = Image.open(imgpath_up) 
        img_up = temp1.resize((45, 50), Image.ANTIALIAS)
        self.up = img_up

        temp2 = Image.open(imgpath_right) 
        img_right = temp2.resize((50, 50), Image.ANTIALIAS)
        self.right = img_right      

        self.left = ImageOps.mirror(img_right)

        self.img = ImageTk.PhotoImage(img_right)
        self.status = "Right"

        self.mode = mode
        self.x = x
        self.y = y
        self.index = x*size + y
        self.pic = None
        self.init_room = self.index
        self.visited = []  
        self.predicted = [(self.index, "-", True)]
        self.wumpus_predited = []

    def display(self, C):
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x == size:
            self.x = size - 1
        if self.y == size:
            self.y = size - 1

        self.index = self.x*size + self.y

        C.delete(self.pic)
        
        self.pic = C.create_image(self.x * unit + 10, self.y * unit + 10, image = self.img, anchor = 'nw')

    def key_move(self, keysym, C):
        if keysym == "Right":
            if self.status == "Right":
                self.x += 1
                self.index += size
            else: 
                self.status = "Right"
            self.img = ImageTk.PhotoImage(self.right)

        elif keysym == "Left":
            if self.status == "Left":
                self.x -= 1
                self.index -= size
            else:
                self.status = "Left"
            self.img = ImageTk.PhotoImage(self.left)

        elif keysym == "Up":
            if self.status == "Up":
                self.y -= 1
                self.index -= 1
            else:
                self.status = "Up"
            self.img = ImageTk.PhotoImage(self.up)
        
        elif keysym == "Down":
            if self.status == "Down":
                self.y += 1
                self.index += 1
            else:
                self.status = "Down"
            self.img = ImageTk.PhotoImage(self.down)

        # node = (self.index, "-", True)
        # if node not in self.visited:
        #     self.visited.append(node)

        self.display(C)

    def facing_to(self, tile, C, top):
        if tile == self.index + size:  # right
            if self.status != "Right":
                self.key_move("Right", C)
        elif tile == self.index - size:  # left
            if self.status != "Left":
                self.key_move("Left", C)
        elif tile == self.index - 1 :  # up
            if self.status != "Up":
                self.key_move("Up", C)
        elif tile == self.index + 1:  # down
            if self.status != "Down":
                self.key_move("Down", C)

        top.update()
        time.sleep(0.2)

    def tile_move(self, tile, C, top):
        self.facing_to(tile,C,top)

        if tile == self.index + size:  # right
            self.key_move("Right", C)

        elif tile == self.index - size:  # left
            self.key_move("Left", C)

        elif tile == self.index - 1 :  # up
            self.key_move("Up", C)

        elif tile == self.index + 1:  # down
            self.key_move("Down", C)

    def action(self, lst, C, top):
        # print("===================")
        # self.print_KB()

        #get_current_index
        Collect = False
        Shoot = False
        path = None
        if "G" in lst[0][1]:
            Collect = True
            lst[0][1].replace("G","")
        if len(lst[0][1]):  #exists
            current_node = (lst[0][0], lst[0][1], True)
        else:
            current_node = (lst[0][0], "-", True)

        lst.pop(0)

        if current_node not in self.visited:
            self.visited.append(current_node)

        #pop it from predicted
        for i in range(len(self.predicted)):
            if current_node[0] == self.predicted[i][0]:
                self.predicted.pop(i)
                break

        #push unvisited node into predicted
        for i in range(0, len(lst)):
            obj = ""
            if "B" in current_node[1]:
                obj += "P"
            if "S" in current_node[1]:
                obj += "W"

            if obj == "":
                next_node = (lst[i], "-", True)
            else:
                next_node = (lst[i], obj, False)

            check_visited = False

            for n in self.visited:  # check if visited
                if next_node[0] == n[0] and type(next_node) == tuple:
                    check_visited = True

            if not check_visited:
                for i in range(len(self.predicted)): # check if predicted
                    if next_node[0] == self.predicted[i][0]:
                        a = self.predicted.pop(i)
                        next_node = TwoToOne(a, next_node)
                        break
                self.predicted.append(next_node)

        # print("visited", self.visited)
        # print("predict", self.predicted)

        #choose next tile
        if self.mode == 'S':
            next_tile = self.choose_next_tile_shy()
        elif self.mode == 'A':
            next_tile, Shoot = self.choose_next_tile_aggressive(current_node[0])

        # print(next_tile)
        if next_tile != -1:
            lst_adj = self.create_lst_adj(next_tile)
            path = A_star(self.index, next_tile, lst_adj)[0]

        return Collect, Shoot, path

    def update_visited(self, tpl):
        for i in range(len(self.visited)):
            if self.visited[i][0] == tpl[0]:
                self.visited.pop(i)
                self.visited.append(tpl)
                break

    def choose_next_tile_shy(self):
        ListPath = []

        for n in self.predicted:
            if n[2] and n[0] != self.index:
                lst_adj = self.create_lst_adj(n[0])
                ListPath.append(A_star(self.index, n[0], lst_adj)[0])
            else:
                ListPath.append(-1)

        min_index = -1
        for i in range(len(ListPath)):
            if ListPath[i] != -1:
                min_index = i
                break 

        for i in range(min_index, len(ListPath)):
            if ListPath[i] != -1 and len(ListPath[i]) < len(ListPath[min_index]):
                min_index = i

        if min_index == -1:
            return -1
        return self.predicted[min_index][0]

    def choose_next_tile_aggressive(self, goal):
        ListPath = []

        for n in self.predicted:
            if n[0] != self.index and "P" != n[1]:         # len!=0 and != Pit and 2nd wumpus
                # print(n)
                # if "W" in n[1] and (n[0],self.index) not in self.wumpus_predited:
                #     self.wumpus_predited.append((n[0],self.index))
                #     print(self.wumpus_predited)
                # else:
                #     lst_adj = self.create_lst_adj(n[0])
                #     ListPath.append(A_star(goal, n[0], lst_adj)[0])
                lst_adj = self.create_lst_adj(n[0])
                ListPath.append(A_star(goal, n[0], lst_adj)[0])
            else:
                ListPath.append(-1)

        min_index = -1
        for i in range(len(ListPath)):
            if ListPath[i] != -1:
                min_index = i
                break 

        for i in range(min_index, len(ListPath)):
            if ListPath[i] != -1 and len(ListPath[i]) < len(ListPath[min_index]):
                min_index = i

        if min_index == -1:
            return -1, False
        
        return self.predicted[min_index][0], not self.predicted[min_index][2]
    
    def create_lst_adj(self, goal):
        lst = []
        for v in self.visited:
            lst.append(v[0])

        lst.append(goal)
        lst_adj = []
        for i in range(size*size):
            temp = []
            if i in lst:
                x,y = i//size,i%size

                if x-1 >= 0 and (x-1)*size + y in lst:       # left
                    temp.append((x-1)*size + y)
                if x+1 < size and (x+1)*size + y in lst:     # right
                    temp.append((x+1)*size + y)
                if y-1 >= 0 and x*size + y -1 in lst:        # Up
                    temp.append(x*size + y -1)
                if y+1 < size and x*size + y +1 in lst:      # Down
                    temp.append(x*size + y +1)    
            lst_adj.append(temp)

        return lst_adj

    def print_KB(self):
        for x in self.visited:
            print(" ", x)
            print("^")
        for x in self.predicted:
            print(" ", x)
            print("^")

    def ClimbOut(self, C,):
        lst_adj = self.create_lst_adj(self.init_room)
        return A_star(self.index, self.init_room, lst_adj)[0]
        

#Wumpus class
class Wumpus (object):
    def __init__(self, imgpath, x, y):
        temp = Image.open(imgpath)
        img2 = temp.resize((unit, unit), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img2)      

        self.x = x
        self.y = y
        self.index = x*size + y
        self.pic = None
        self.ListStench = []
        self.create_stench()

    def create_stench(self):
        s = Stench("../IMAGE/stench.png", self.x-1 ,self.y)
        self.ListStench.append(s)
        s = Stench("../IMAGE/stench.png", self.x+1 ,self.y)
        self.ListStench.append(s)
        s = Stench("../IMAGE/stench.png", self.x ,self.y-1)
        self.ListStench.append(s)
        s = Stench("../IMAGE/stench.png", self.x ,self.y+1)
        self.ListStench.append(s)

    def display(self, C):
        self.pic = C.create_image(self.x * unit, self.y * unit, image = self.img, anchor = 'nw')

    def destroy(self, C):
        C.delete(self.pic)
        while self.ListStench:
            del self.ListStench[0]

    def find_stench(self, index, C):
        for s in self.ListStench:
            if s.index == index:
                s.display(C)
                return True
        return False

#Pit class  
class Pit (object):
    def __init__(self, imgpath, x, y):
        temp = Image.open(imgpath)
        img2 = temp.resize((unit, unit), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img2)      

        self.x = x
        self.y = y
        self.index = x*size + y
        self.pic = None
        
    def display(self, C):
        self.pic = C.create_image(self.x * unit, self.y * unit, image = self.img, anchor = 'nw')

#Stench class
class Stench (object):
    def __init__(self, imgpath, x, y):
        temp = Image.open(imgpath)
        img2 = temp.resize((unit, int(unit/2)), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img2)      

        self.x = x
        self.y = y
        self.index = x*size + y
        self.pic = None
        
    def display(self, C):
        self.pic = C.create_image(self.x * unit, self.y * unit, image = self.img, anchor = 'nw')

    def destroy (self, C):
        C.delete(self.pic)
    
#Gold class
class Gold (object):
    def __init__(self, imgpath, x, y):
        temp = Image.open(imgpath)
        img2 = temp.resize((unit, unit), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img2)      

        self.x = x
        self.y = y
        self.index = x*size + y
        self.pic = None
        
    def display(self, C):
        self.pic = C.create_image(self.x * unit, self.y * unit, image = self.img, anchor = 'nw')

    def destroy (self, C):
        C.delete(self.pic)

#Breeze class
class Breeze (object):
    def __init__(self, imgpath, x, y):
        temp = Image.open(imgpath)
        img2 = temp.resize((unit, int(unit/2)), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img2)      

        self.x = x
        self.y = y
        self.index = x*size + y
        self.pic = None
        
    def display(self, C):
        self.pic = C.create_image(self.x * unit, self.y * unit + unit/2, image = self.img, anchor = 'nw')

#Brick
class Brick (object):
    def __init__(self, imgpath, x, y):
        temp = Image.open(imgpath)
        img2 = temp.resize((unit, unit), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img2)      

        self.x = x
        self.y = y
        self.index = x*size + y
        self.pic = None
        
    def display(self, C):
        self.pic = C.create_image(self.x * unit, self.y * unit, image = self.img, anchor = 'nw')

    def destroy(self, C):
        C.delete(self.pic)

#Door
class door(object):
    def __init__(self,x,y):
        temp = Image.open("../IMAGE/door.png")
        img2 = temp.resize((unit, unit), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img2)    
        self.x = x
        self.y = y
        self.index = x*size + y
        self.pic = None

    def display(self, C):
        self.pic = C.create_image(self.x * unit, self.y * unit, image = self.img, anchor = 'nw')

#laser
class laser(object):
    def __init__(self,x,y):
        temp = Image.open("../IMAGE/laser.png")
        img1 = temp.resize((5, unit), Image.ANTIALIAS)
        img2 = temp.resize((unit, 5), Image.ANTIALIAS)
 
        self.vertical = ImageTk.PhotoImage(img1)   
        self.horizontal = ImageTk.PhotoImage(img2)

        self.x = x
        self.y = y
        self.pic = None

    def display(self, C, status):
        if status == "Right" :
            self.pic = C.create_image(self.x * (unit) + 50, self.y * (unit) + unit/2, image = self.horizontal, anchor = 'nw')
        elif status == "Left":
            self.pic = C.create_image(self.x * (unit) - 50, self.y * (unit) + unit/2, image = self.horizontal, anchor = 'nw')
        elif status == "Down":
            self.pic = C.create_image(self.x * (unit) + unit/2, self.y * (unit) + 50, image = self.vertical, anchor = 'nw')
        else:
            self.pic = C.create_image(self.x * (unit) + unit/2, self.y * (unit) - 50, image = self.vertical, anchor = 'nw')

    def destroy(self, C):
        C.delete(self.pic)
