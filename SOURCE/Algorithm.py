import numpy as np

def TwoToOne(a,b):
    if (not a[2]) and (not b[2]) and (a[1] in b[1] or b[1] in a[1]):
        if len(a[1]) < len(b[1]):
            return a
        else:
            return b
    
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

def path(explored, node, begin, file):
    path = [node]
    adj_list = file
    while (node != begin):
        for i in range(len(explored)):
            if node in adj_list[explored[i]]:
                path.append(explored[i])
                node = explored[i]
                break
    path.reverse()
    return path

def A_star(begin, goal, file):
    # 5 -> 16
    explored,frontier = [],[(0,begin)] 
    while(frontier):
        index = pop_lowest(frontier)
        node = frontier.pop(index)
        explored.append(node[1]) 

        if (explored[-1]==goal):
            return [path(explored, goal, begin, file), explored, len(explored)]

        for j in file[node[1]]:
            if check_exist(j,frontier)==0:
                if j not in explored:
                    frontier.append((node[0] - manhattan(node[1],goal) + 1 + manhattan(j,goal) ,j))
    return False  # cannot found
    