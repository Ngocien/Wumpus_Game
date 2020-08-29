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
        self.visited = [(self.index, "-", T)]   #(current, parent)
        self.predicted = []

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

        self.display(C)

    def tile_move(self, tile, C):
        if tile == self.index + size:  # right
            self.key_move("Right", C)

        elif tile == self.index - size:  # left
            self.key_move("Left", C)

        elif tile == self.index - 1:  # up
            self.key_move("Up", C)

        elif tile == self.index + 1:  # down
            self.key_move("Down", C)
 
    def print_KB(self):
        for x in self.visited:
            print(x)
            print("^")
        for x in self.predicted:
            print(x)
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
