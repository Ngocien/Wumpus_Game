from PIL import ImageTk, Image, ImageOps
import time, random
unit = 70
size = 10
# Pacman object
class Agent(object):
    def __init__(self, imgpath_down, imgpath_up, imgpath_right, x, y):
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

        self.x = x
        self.y = y
        self.index = x*size + y
        self.pic = None
        self.init_room = self.index
        self.visited = []  
        self.predicted = [(self.index, "-", True)]

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

        node = (self.index, "-", True)
        if node not in self.visited:
            self.visited.append(node)

        self.display(C)

    def tile_move(self, tile, C, top):
        if tile == self.index + size:  # right
            if self.status != "Right":
                self.key_move("Right", C)
                top.update()
                time.sleep(0.5)
            self.key_move("Right", C)

        elif tile == self.index - size:  # left
            if self.status != "Left":
                self.key_move("Left", C)
                top.update()
                time.sleep(0.5)
            self.key_move("Left", C)

        elif tile == self.index - 1 :  # up
            if self.status != "Up":
                self.key_move("Up", C)
                top.update()
                time.sleep(0.5)
            self.key_move("Up", C)

        elif tile == self.index + 1:  # down
            if self.status != "Down":
                self.key_move("Down", C)
                top.update()
                time.sleep(0.5)
            self.key_move("Down", C)

        top.update()

    def action(self, lst, C, top):
        #get_current_index
        Collect = False
        if lst[0][1] == "G":
            Collect = True
            current_node = (lst[0][0], "-", True)
        else:
            current_node = (lst[0][0], lst[0][1], True)

        self.visited.append(current_node)
        lst.pop(0)

        # A_star,path[i]
        self.tile_move(current_node[0], C, top)

        #pop it from predicted
        for i in range(len(self.predicted)):
            if current_node == self.predicted[i]:
                self.predicted.pop(i)
                break

        #push unvisited node into predicted
        for i in range(0, len(lst)):
            if current_node[1] == "-":
                next_node = (lst[i], "-", True)
            elif current_node[1] == "B":
                next_node = (lst[i], "P", False)
            elif current_node[1] == "S":
                next_node = (lst[i], "W", False)

            if next_node not in self.visited:
                self.predicted.append(next_node)

        next_tile = self.update_predicted_list()

        return Collect, next_tile

    def update_predicted_list(self):

        self.predicted.sort()
        print(self.predicted)
        # self.print_KB()
        next_tile = -1
        for n in self.predicted:
            if n[2]:
                next_tile = n[0]
                break
        print(next_tile)
        return next_tile

    def print_KB(self):
        for x in self.visited:
            print(" ", x)
            print("^")
        for x in self.predicted:
            print(" ", x)
            print("^")


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
