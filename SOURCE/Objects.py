from PIL import ImageTk, Image, ImageOps
import time, random
unit = 25
size = 10
# Pacman object
class Agent(object):
    def __init__(self, imgpath_down, imgpath_up, imgpath_right, x, y):
        temp = Image.open(imgpath_down) 
        img_down = temp.resize((25, 25), Image.ANTIALIAS)
        self.down = img_down

        temp1 = Image.open(imgpath_up) 
        img_up = temp1.resize((25, 25), Image.ANTIALIAS)
        self.up = img_up

        temp2 = Image.open(imgpath_right) 
        img_right = temp2.resize((25, 25), Image.ANTIALIAS)
        self.right = img_right      

        self.left = ImageOps.mirror(img_down)

        self.img = ImageTk.PhotoImage(img_right)
        self.x = x
        self.y = y
        self.index = x*size + y
        self.pic = None
        self.visited = [(self.index, -1)]   #(current, parent)

    

    def display(self, C):
        C.delete(self.pic)

        self.pic = C.create_image(self.x * unit, self.y * unit, image = self.img, anchor = 'nw')

    def key_move(self, keysym, C):
        if keysym == "Right":
            self.x += 1
            self.index += size
            self.img = ImageTk.PhotoImage(self.right)
        elif keysym == "Left":
            self.x -= 1
            self.index -= size
            self.img = ImageTk.PhotoImage(self.left)
        elif keysym == "Up":
            self.y -= 1
            self.index -= 1
            self.img = ImageTk.PhotoImage(self.up)
        elif keysym == "Down":
            self.y += 1
            self.index += 1
            self.img = ImageTk.PhotoImage(self.down)

        self.display(C)

    def path_move(self, tile, C):
        if tile == self.index + size:  # right
            self.key_move("Right", C)

        elif tile == self.index - size:  # left
            self.key_move("Left", C)

        elif tile == self.index - 1:  # up
            self.key_move("Up", C)

        elif tile == self.index + 1:  # down
            self.key_move("Down", C)

#Wumpus class
class Wumpus (object):
    def __init__(self, imgpath, x, y):
        temp = Image.open(imgpath)
        img2 = temp.resize((25, 25), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img2)      

        self.x = x
        self.y = y
        self.index = x*size + y
        self.pic = None
        
    def display(self, C):
        self.pic = C.create_image(self.x * unit, self.y * unit, image = self.img, anchor = 'nw')

#Pit class
class Pit (object):
    def __init__(self, imgpath, x, y):
        temp = Image.open(imgpath)
        img2 = temp.resize((25, 25), Image.ANTIALIAS)
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
        img2 = temp.resize((25, 25), Image.ANTIALIAS)
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
        img2 = temp.resize((25, 25), Image.ANTIALIAS)
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
        img2 = temp.resize((25, 25), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img2)      

        self.x = x
        self.y = y
        self.index = x*size + y
        self.pic = None
        
    def display(self, C):
        self.pic = C.create_image(self.x * unit, self.y * unit, image = self.img, anchor = 'nw')






