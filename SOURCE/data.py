import numpy as np
def get_maze(filename):
    f = open(filename, 'r')
    maze = []
    size = f.readline()
    temp = f.readlines()
    for i in range(len(temp)):
        maze.append(temp[i].rstrip('\n').split('.'))
    return maze, int(size)

maze , size = get_maze("../DATA/maze01.txt")


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
            list_adj.append(temp)
    return list_adj    


def scan_maze(maze, size):
    wumpus, pit, breeze, stench, gold = [], [] ,[] ,[] ,[]
    agent = None
    for i in range(size):
        for j in range(size):
            if maze[i][j] == 'W':
                w = Wumpus("../IMAGE/Wumpus.png", j ,i)
                wumpus.append(w)
            elif maze[i][j] == 'P':
                p = Pit("../IMAGE/pit.png", j ,i)
                pit.append(p)
            elif maze[i][j] == 'B':
                b = Breeze("../IMAGE/breeze.png", j ,i)
                breeze.append(b)
            elif maze[i][j] == 'G':
                g = Gold("../IMAGE/gold.png", j ,i)
                gold.append(g)
            elif maze[i][j] == 'S':
                s = Stench("../IMAGE/stench.png", j ,i)
                stench.append(s)
            elif maze[i][j] == 'A':
                agent = Agent("../IMAGE/Agent_D.png","../IMAGE/Agent_U.png","../IMAGE/Agent_R.png", j ,i)
