import numpy as np
from Objects import *

def get_maze(filename):
    f = open(filename, 'r')
    maze = []
    size = f.readline()
    temp = f.readlines()
    for i in range(len(temp)):
        maze.append(temp[i].rstrip('\n').split('.'))
    return maze, int(size)

def scan_index(maze,size):
    list_adj = []
    for i in range(len(maze)): #i là dòng
        for j in range(len(maze)): #j là cột
            temp = []
            if i==0 and j ==0: # gốc trái trên
                temp.append(((i+1)*10,maze[i+1][j]))
                temp.append(((j+1),maze[i][j+1]))

            elif i==0 and j==size-1: #gốc phải trên
                temp.append(((i+1)*10+j,maze[i+1][j]))
                temp.append((j-1,maze[i][j-1]))

            elif j== 0 and i== size -1: #gốc trái dưới
                temp.append(((i-1)*10,maze[i-1][j]))
                temp.append((i*10+j+1,maze[i][j+1]))

            elif j==size-1 and i== size -1: #gốc trái trên
                temp.append((((i-1)*10+j),maze[i-1][j]))
                temp.append(((i*10+j-1),maze[i][j-1]))

            elif j==0 : #cột đầu tiên
                temp.append(((i-1)*10,maze[i-1][j]))
                temp.append(((i+1)*10,maze[i+1][j]))
                temp.append((i*10+j+1,maze[i][j+1]))

            elif i==0: #dòng đầu tiên
                temp.append((j-1,maze[i][j-1]))
                temp.append((j+1,maze[i][j+1]))
                temp.append(((i+1)*10+j,maze[i+1][j]))

            elif i==size-1: #dòng cuối cùng
                temp.append(((i)*10+j-1,maze[i][j-1]))
                temp.append(((i)*10+j+1,maze[i][j+1]))
                temp.append(((i-1)*10+j,maze[i-1][j]))

            elif j==size-1: #cột cuối cùng
                temp.append(((i-1)*10+j,maze[i-1][j]))
                temp.append(((i+1)*10+j,maze[i+1][j]))
                temp.append(((i)*10+j-1,maze[i][j-1]))

            else: #còn lại
                temp.append(((i-1)*10+j,maze[i-1][j]))
                temp.append(((i+1)*10+j,maze[i+1][j]))
                temp.append(((i)*10+j-1,maze[i][j-1]))
                temp.append((i*10+j+1,maze[i][j+1]))
            temp.sort()
            list_adj.append(temp)
    return list_adj    

def scan_maze(maze, size):
    wumpus, pit, breeze, gold, brick = [], [] ,[] ,[] ,[]
    agent = None
    for i in range(size):
        for j in range(size):
            br = Brick("..//IMAGE/brick.png", j, i)
            brick.append(br)
            for t in maze[i][j]:
                if t == 'W':
                    w = Wumpus("../IMAGE/Wumpus.png", j ,i)
                    wumpus.append(w)
                if t == 'P':
                    p = Pit("../IMAGE/pit.png", j ,i)
                    pit.append(p)
                if t == 'B':
                    b = Breeze("../IMAGE/breeze.png", j ,i)
                    breeze.append(b)
                if t == 'G':
                    g = Gold("../IMAGE/gold.png", j ,i)
                    gold.append(g)
                if t == 'A':
                    agent = Agent("../IMAGE/Agent_D.png","../IMAGE/Agent_U.png","../IMAGE/Agent_R.png", j ,i)

    return agent, wumpus, pit, breeze, gold, brick

def random_Maze():
    size = 10
    maze = []

    objects = ["-", "-", "-", "P", "-", "-", "W", "-", "-", "G", "-", "-"]

    for i in range(size):
        temp = []
        for _ in range(size):
            o = np.random.randint(0,len(objects))
            temp.append(objects[o])

        maze.append(temp)


    for i in range(size):
        for j in range(size):
            if "P" in maze[i][j]:
                if i > 0 and "B" not in maze[i-1][j] and "P" not in maze[i-1][j]:
                    maze[i-1][j] += "B"
                if i+1 < size and "B" not in maze[i+1][j] and "P" not in maze[i+1][j] :
                    maze[i+1][j] += "B"
                if j > 0 and "B" not in maze[i][j-1] and "P" not in maze[i][j-1]:
                    maze[i][j-1] += "B"
                if j+1 < size and "B" not in maze[i][j+1] and "P" not in maze[i][j+1]:
                    maze[i][j+1] += "B"
            
            elif "W" in maze[i][j]:
                if i > 0 and "S" not in maze[i-1][j] and "W" not in maze[i-1][j]:
                    maze[i-1][j] += "S"
                if i+1 < size and "S" not in maze[i+1][j] and "W" not in maze[i+1][j] :
                    maze[i+1][j] += "S"
                if j > 0 and "S" not in maze[i][j-1] and "W" not in maze[i][j-1]:
                    maze[i][j-1] += "S"
                if j+1 < size and "S" not in maze[i][j+1] and "W" not in maze[i][j+1]:
                    maze[i][j+1] += "S"

    x = 0
    y = 0
    while maze[x][y] != "-":
        x = np.random.randint(0, size)
        y = np.random.randint(0, size)

    maze[x][y] = "A"

    return maze,size
