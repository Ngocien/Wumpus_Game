import numpy as np
def get_maze(filename):
    f = open(filename, 'r')
    maze, size= [],[]
    size = f.readline()
    temp = f.readlines()
    for i in range(len(temp)):
        maze.append(temp[i].rstrip('\n').split('.'))
    return maze, int(size)

maze , size = get_maze("maze01.txt")

def scan_maze(maze,size):
    list_adj = []
    for i in range(size): #i là dòng
        for j in range(size): #j là cột
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
list_adj = scan_maze(maze,size)         

def check(obj, array):
    for i in range(len(array)):
        if obj in array[i]:
            return True
list_adj = scan_maze(maze,size)          

def list_obj (obj, list_adj):
    lisst= []
    for i in range(len(list_adj)):
        for j in range(len(list_adj[i])):
            if len(list_adj[i][j][1]) != 1 and check(obj,list_adj[i][j][1])== True:
                if list_adj[i][j][0] not in lisst:
                    lisst.append(list_adj[i][j][0])
                    
            elif len(list_adj[i][j][1]) == 1 and obj in list_adj[i][j][1]:
                if list_adj[i][j][0] not in lisst:
                    lisst.append(list_adj[i][j][0])
    return lisst

list_wumpus = list_obj('W', list_adj)
print("list_wumpus", list_wumpus)

list_breeze = list_obj('B', list_adj)
print("list_breeze", list_breeze)

list_pit = list_obj('P', list_adj)
print("list_pit", list_pit)

list_stench = list_obj('S', list_adj)
print("list_stench", list_stench)

list_gold = list_obj('G', list_adj)
print("list_gold", list_gold)

    
