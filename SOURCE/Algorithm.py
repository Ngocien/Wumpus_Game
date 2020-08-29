import numpy as np


def TwoToOne(a,b):
    if not a[2] and not b[2]  and a[1]== b[1]:
        return a
    else:
        return (a[0],'-',True)

def manhattan(now, after):
	return abs(now // 10 - after // 10 ) + abs(now % 10 - after % 10)

def pop_lowest(frontier):
    lowest = 0
    for i in range(len(frontier)): #i la tuple (priority,node)
        if (frontier[i][0] < frontier[lowest][0]):
            lowest=i
    return lowest

def check_exist(node,frontier):
    for i in frontier:
        if(node == i[1]):
            return 1
    return 0     


def path(explored, node):
    path = [node]
    adj_list = file
    while (node !=0):
        for i in range(len(explored)):
            if node in adj_list[explored[i]]:
                path.append(explored[i])
                node = explored[i]
                break
    path.reverse()
    return path
    

def A_star(visited, goal):
    explored, frontier = [],[(0,0)]
    while (frontier):
        index = pop_lowest(frontier)
        print("index",index)
        node = frontier.pop(index)
        explored.append(node[1])
        print("node", node)
        if explored[-1] == goal:
            return path(explored,goal)
        
        for i in visited:
            if check_exist (i, frontier) == 0:
                if i not in explored:
                    frontier.append((node[0] - manhattan(node[1], goal) + 1 + manhattan(i,goal) , i)) #(priority, node)
    return False

temp = [(8),(7,9),(6,8),(5,7,16),(6)]

print(A_star(temp, 16))