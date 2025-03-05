# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)

import heapq
import sys
from copy import copy

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)


def sanity_check(maze, path):
    """
    Runs check functions for part 0 of the assignment.

    @param maze: The maze to execute the search on.
    @param path: a list of tuples containing the coordinates of each state in the computed path

    @return bool: whether or not the path pass the sanity check
    """
    # TODO: Write your code here
    return False


def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    print("TESSSSTTTING")
    node = maze.getStart()
    if maze.isObjective(node[0],node[1]):
        solution = [node]
        return solution

    print("HEEELLLLOOO")
    # create traversal queue
    bfs_Q = []
    # create a visited list
    visited = []
    # # create the distance dictionary
    # dist = {}
    # create the predecessor dictionary
    pred = {}
    # create the return path
    path = []
    bfs_Q.append(node)  # add the start node to the queue
    # path.append(node)
    # dist[node] = 0  # set start distance to zero

    done = False   # signals when to end the BFS
    print("START_VAL",node)

    # BFS loop
    while len(bfs_Q) != 0:      # while the traversal list is not empty     and maze.isObjective(node[0],node[1]) == False
        node = bfs_Q[0]         # load the first element into the current node
        del bfs_Q[0]            # pop off the first element in the list
        visited.append(node)
        # print("CUR_NODE",node)
        for i in maze.getNeighbors(node[0],node[1]):  # get the neighbors of node
            child_node = i
            # print("CHILD", child_node)
            # print("Parent", node)
            if child_node not in visited and child_node not in bfs_Q:
                if maze.isObjective(child_node[0],child_node[1]):     #check if it is the goal state
                    done = True
                    pred[child_node] = node
                    node = child_node       # node == Goal State
                    # print("GOAL_FOUND", node)
                    break        
                else:
                    if child_node not in visited:
                        pred[i] = node                   # set the predecessor for the neighbor/child
                    bfs_Q.append(i)     # add neighbors to traversal list

        if done:  # goal state found, so end BFS
            break

    else:       # if there is no path to the goal, return an empty list
        return []    

    # backtrack through the predecessor list to generate the path
    backtrack = node
    path.append(node)
    # print("GOAL2",backtrack," ","GOAL_PRED", pred[backtrack])
    # print(pred)
    while backtrack != maze.getStart():
        path.insert(0,pred[backtrack])
        # print("LOOP", pred[backtrack])
        backtrack = pred[backtrack]

    if path[0] != maze.getStart(): #safety check that the start node is at the front of the list
        path.insert(0,pred[backtrack])
    # print(path)
    return path

def Manhattan(node,goal):   # h(x) function
    # print("HHHHIIIII")
    # print(type(node[0]), type(node[1]))
    # print(type(goal[0]), type(goal[1]))
    dx = abs(node[0] - goal[0])
    dy = abs(node[1] - goal[1])
    return 1 * (dx + dy)

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    path = []
    # create the priorty Queue, queue is a tuple (f(x), g(x), state)
    frontier = []
    heapq.heapify(frontier)
    # dictionary for the done/closed states: key= node, val= priority
    visited = {}
    # intialize a predecessor dictionary
    pred = {}
    # get list of objectives
    goals = maze.getObjectives()

    done = False # signal to end the loop

    # single node case check, redunadancy
    node = maze.getStart()
    if maze.isObjective(node[0],node[1]):
        solution = [node]
        return solution


    start_h = Manhattan(node,goals[0])
    start_prior = (start_h, 0, node)   # (f(x), g(x), start)
    heapq.heappush(frontier,start_prior)

    while len(frontier) != 0:
        
        
        # for x in frontier:
        #     if x[0] != priority[0]: break
        #     if x[1] < priority[1]: priority = x # if f(x) == f(Q_Top), check if g(x) is smaller that g(Q_top)

        # frontier.remove(priority)
        priority = heapq.heappop(frontier)  # remove the element with ther highest priority
        node = priority[2]
        visited[node] = priority[0] # add it to the closed list
        # print("cur_node", node)
        #neighbor loop
        neighbors = maze.getNeighbors(node[0],node[1])
        for i in neighbors:
            child_node = i
            # print("CHILD", child_node)
            # print("Parent", node)

            #priority Check
            # print("frontier ",frontier)
            g = priority[1] + 1      # update distance from start
            h = Manhattan(child_node,goals[0])
            f = g + h
            new_priority = (f, g ,child_node)  # (f(x), g(x), child)

            
            if child_node not in visited and new_priority not in frontier:     # add to frontier if not visited or in priority queue
                if maze.isObjective(child_node[0],child_node[1]):     #check if it is the goal state
                    done = True
                    pred[child_node] = node
                    node = child_node       # node == Goal State
                    # print("GOAL_FOUND", node)
                    break  
                else:
                    # if child_node not in visited:
                    pred[i] = node                   # set the predecessor for the neighbor/child
                    heapq.heappush(frontier, new_priority)     # add neighbors to frontier list
                    # frontier.sort(reverse=False)      # sort the priority queue
                    # print("frontier = ", frontier)

        if done:  # goal state found, so end A* search
            break
       
    # else:       # if there is no path to the goal, return an empty list
    #     return []    

    # backtrack through the predecessor list to generate the path
    backtrack = node
    path.append(node)
    # print("GOAL2",backtrack," ","GOAL_PRED", pred[backtrack])
    # print(pred)
    while backtrack != maze.getStart():
        path.insert(0,pred[backtrack])
        # print("LOOP", pred[backtrack])
        backtrack = pred[backtrack]

    if path[0] != maze.getStart(): #safety check that the start node is at the front of the list
        path.insert(0,pred[backtrack])
    # print(path)
    return path

def M_of_M(node,goals):

    goal_list = list(goals)
    if node in goals:
        goal_list.remove(node)
    nearest = []
    nearest2 = []
    # print("node ", node)
    nearest_goal_val = 0 # initialize value
    nearest_goal = (0,0)
    nearest_2_val = 0 # initialize value
    nearest_2 = (0,0)

    other_goals = 0
    another_goals = 0
    for obj in goals:       # find the manhattan distance from cur_node to nearest goal
        if nearest_goal_val == 0:
            nearest_goal_val = Manhattan(node,obj)
            nearest_goal = obj  # the nearest goal to cur_node
        x = Manhattan(node,obj)
        if x < nearest_goal_val:
            nearest_goal_val = x
            nearest_goal = obj  # update the nearest goal to cur_node
    # print("nearest_goal ", nearest_goal, " = ", nearest_goal_val)
    if nearest_goal in goal_list:
        goal_list.remove(nearest_goal)
    # print("HI", len(goal_list))
    for obj in goal_list:       # find the manhattan distance from nearest_goal to next nearest goal
        nearest_2_val = Manhattan(nearest_goal,obj)
        nearest.append(nearest_2_val)

    # print("nearest_vals ", nearest)
    for x in nearest:
        other_goals = other_goals + x


    # while len(goal_list) != 0:
    #     for obj in goal_list:       # find the manhattan distance from nearest_goal to next nearest goal
    #         if nearest_2 == (0,0):
    #             nearest_2_val = Manhattan(nearest_goal,obj)
    #             nearest_2 = obj
    #         else:
    #             x = Manhattan(nearest_goal,obj)
    #             if x < nearest_2_val:
    #                 nearest_2_val = x
    #                 nearest_2 = obj

    #     nearest2.append(nearest_2_val)
    #     goal_list.remove(nearest_2)
    #     nearest_goal = nearest_2
    #     nearest_2_val = 0 # initialize value
    #     nearest_2 = (0,0)

    # for x in nearest2:
    #     another_goals = another_goals + x 

    # if(another_goals > other_goals): return another_goals
    # else: return other_goals

    # print("BAD_PRINT")
    return  other_goals

def backtracking(end, pred, start, goals):    
    path = []
    backtrack = end
    goal_count = 0
    # path.append(end[0])
    # if len(cur_path) == 0: path.append(end[2])
    # elif cur_path[-1] != end[2]: 
        # print("cur_path[end]", cur_path[-1])
        # print("cur_start", start)
        # print("cur_GOAL", node)
        # path.append(end[2])
    # print("START",start)
    # print('backtrack', backtrack)
    # print("cur_path ", cur_path)
    while backtrack[0] != start or len(backtrack[1]) != 4:
        # print("BREAK", 'pred[backtrack]', pred[backtrack])
        pred_state = pred[backtrack]
        # if pred_state[2] in goals:
        #     goal_count += 1
        #     print("GOAL_COUNT = ", goal_count)
        path.insert(0,backtrack[0])
        # print("LOOP", pred[backtrack])
        backtrack = pred[backtrack]
        # print('backtrack', backtrack)
    # if len(path) > 0 and start in pred:
    if path[0] != start: #safety check that the start node is at the front of the list
        # print("len(path)", len(path))
        path.insert(0,start)
    # elif path[0] != start: #safety check that the start node is at the front of the list
    #     path.insert(0,pred[backtrack])

    return path

    
def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here

    # initialize return list
    path = []
    # create the priorty Queue, queue is a tuple (f(x), g(x), state)
    frontier = []
    heapq.heapify(frontier)
    # dictionary for the done/closed states: key= node, val= priority
    visited = {}
    # intialize a predecessor dictionary
    pred = {}
    # get list of objectives
    goals = maze.getObjectives()

    done = False # signal to end the loop

    node = maze.getStart()
    start_h = M_of_M(node,goals)
    temp_goals = goals.copy()
    # temp_goals.sort()
    start_prior = (start_h, 0,node, tuple(temp_goals))   # (f(x), g(x), start, # of goals left)
    heapq.heappush(frontier,start_prior)
    pred[(node, tuple(temp_goals))] = None
    start_node = node  # the starting node for the current path, 
    end_state  = start_prior

    # while len(frontier) != 0:
    #     priority = heapq.heappop(frontier)  # remove the element with ther highest priority
    #     node = priority[3]
    #      if maze.isObjective(node[0],node[1]) and node in goals:
    #         goals.remove(node)
    #         if len(goals) == 0:
    #             done = True
    #             end_state = new_priority
    #             break
            


    #     visited[priority] = priority[0]




    while len(frontier) != 0:
        priority = heapq.heappop(frontier)  # remove the element with ther highest priority
        node = priority[2]
        parent_goals = priority[3]
        # parent_goals.sort()
        visit_parent = (node, tuple(parent_goals))
        visited[visit_parent] = priority[1]   # g(x)
        # figure out the order of Ojectives to visit
        # goals = M_of_M(node,goals)


        neighbors = maze.getNeighbors(node[0],node[1])
        for i in neighbors:
            child_node = i
            g = priority[1] + 1      # update distance from start
            h = M_of_M(child_node,parent_goals)
            f = h + g
            child_goals = copy(parent_goals)
            visit_child = (child_node, child_goals)
            new_priority = (f, g , child_node, child_goals)  # (f(x), g(x), child, list goals left)

            if visit_child not in visited and new_priority not in frontier:     # add to frontier if not visited or in priority queue
                if maze.isObjective(child_node[0],child_node[1]) and child_node in parent_goals:     #check if it is the goal state

                    # print("HI", pred)
                    node = child_node       # node == Goal State
                    child_goals  = list(child_goals)
                    child_goals.remove(node)      #remove goal from the goals copy list
                    child_goals  = tuple(child_goals)
                    visit_child = (child_node, child_goals)  # rebuild the child state
                    new_priority = (f, g , child_node, child_goals)

                    pred[visit_child] = visit_parent

                    start_node = node      # reset the start node to the goal I am at
                    if len(child_goals) == 0:
                        done = True
                        end_state = visit_child
                        # print ("end_state", end_state)
                        break

                    heapq.heappush(frontier, new_priority)     # add neighbors to frontier list
                else:
                    # if new_priority not in pred:
                    pred[visit_child] = visit_parent                   # set the predecessor for the neighbor/child
                    heapq.heappush(frontier, new_priority)     # add neighbors to frontier list 
                    # else:
                    #     heapq.heappush(frontier, new_priority)          

            elif  visit_child in visited and visited[visit_child] >  g:
                # if maze.isObjective(child_node[0],child_node[1]) and child_node in parent_goals:     #check if it is the goal state

                #     # print("HI", pred)
                #     node = child_node       # node == Goal State
                #     child_goals  = list(child_goals)
                #     child_goals.remove(node)      #remove goal from the goals copy list
                #     child_goals  = tuple(child_goals)
                #     visit_child = (child_node, child_goals)  # rebuild the child state
                #     new_priority = (f, g , child_node, child_goals)

                #     pred[visit_child] = visit_parent

                #     start_node = node      # reset the start node to the goal I am at
                #     if len(child_goals) == 0:
                #         done = True
                #         end_state = visit_child
                #         # print ("end_state", end_state)
                #         break

                #     heapq.heappush(frontier, new_priority)     # add neighbors to frontier list
                # else:
                    # if new_priority not in pred:
                    pred[visit_child] = visit_parent                   # set the predecessor for the neighbor/child
                    heapq.heappush(frontier, new_priority)     # add neighbors to frontier list 

        if done:  # goal state found, so end A* search
            break
    
    # # backtrack through the predecessor list to generate the path
    # backtrack = node
    # path.append(node)
    # # print("GOAL2",backtrack," ","GOAL_PRED", pred[backtrack])
    # # print(pred)
    # while backtrack != maze.getStart():
    #     path.insert(0,pred[backtrack])
    #     # print("LOOP", pred[backtrack])
    #     backtrack = pred[backtrack]

    # if path[0] != maze.getStart(): #safety check that the start node is at the front of the list
    #     path.insert(0,pred[backtrack])

    path = path + backtracking(end_state,pred,maze.getStart(),maze.getObjectives())
    # print(path)
    # print(backtracking(end_state,pred,maze.getStart(),maze.getObjectives()))
    # print("valid_path: ",maze.isValidPath(path))

    return path

def Prim_MST(goals):
    vertices = []
    Pred = {}
    solution = 0

    for i in goals:
        vertices.append((sys.maxsize, i))  # state = (weight, node)
    # print("goals = ",goals)
    vert = vertices[0][1]
    vertices[0] = (0, vert) # initialize the first element in the MST
    vertices.sort()
    Pred[vertices[0][1]] = None

    while len(vertices) != 0:
        v = vertices[0]
        v_node = v[1]
        vertices.remove(v)
        
        if Pred[v_node] != None:
            solution = solution + Manhattan(Pred[v_node], v_node)

        for u in vertices:
            if Manhattan(v_node, u[1]) < u[0]:
                vertices.remove(u)
                u = (Manhattan(v_node, u[1]), u[1])
                vertices.append(u)
                Pred[u[1]] = v_node
        vertices.sort()
        # print("vertices", vertices)

    # print("Pred", Pred)
    # print("solution_value", solution)
    return solution

def closest_goal(node, goals):
    goal_list = list(goals)
    if node in goals:
        goal_list.remove(node)
    # print("node ", node)
    nearest_goal_val = 0 # initialize value
    nearest_goal = (0,0)

    for obj in goals:       # find the manhattan distance from cur_node to nearest goal
        if nearest_goal_val == 0:
            nearest_goal_val = Manhattan(node,obj)
            nearest_goal = obj  # the nearest goal to cur_node
        x = Manhattan(node,obj)
        if x < nearest_goal_val:
            nearest_goal_val = x
            nearest_goal = obj  # update the nearest goal to cur_node
    
    return nearest_goal_val

def backtrack_MST(end, pred, start, goals):    
    path = []
    backtrack = end
    goal_count = 0

    # print("END_STATE", end)
    # print("START_STATE", start)
    # print("len(GOALS)= ", len(goals))

    while backtrack[0] != start or len(backtrack[1]) != len(goals)- 1  :
        # print("len(goals) = ", len(backtrack[1]))
        # print("BREAK", 'pred[backtrack]', pred[backtrack])
        pred_state = pred[backtrack]
        path.insert(0,backtrack[0])
        if pred_state[0] == start and len(pred_state[1]) == len(goals):
            # print("BREAK_OUT", 'pred_state', pred_state)
            # print("len(goals) = ", len(pred_state[1]))
            break
        backtrack = pred[backtrack]
    # if len(path) > 0 and start in pred:
    if path[0] != start: #safety check that the start node is at the front of the list
        path.insert(0,start)

    return path

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

   # initialize return list
    path = []
    # create the priorty Queue, queue is a tuple (f(x), g(x), state)
    frontier = []
    heapq.heapify(frontier)
    # dictionary for the done/closed states: key= node, val= priority
    visited = {}
    # intialize a predecessor dictionary
    pred = {}
    # get list of objectives
    goals = maze.getObjectives()
    # MST_values for each set of goals
    goals_MST = {}

    done = False # signal to end the loop

    node = maze.getStart()
    mst_val = Prim_MST(goals)
    start_h =  mst_val
    temp_goals = goals.copy()
    goals_MST[tuple(temp_goals)] = mst_val
    # temp_goals.sort()
    start_prior = (start_h, 0,node, tuple(temp_goals))   # (f(x), g(x), start, # of goals left)
    heapq.heappush(frontier,start_prior)
    pred[(node, tuple(temp_goals))] = None
    start_node = node  # the starting node for the current path, 
    end_state  = start_prior

    count = 0
    # prim_count = 0
    loop = 0

    while len(frontier) != 0 or loop != 500:
        # print("LLLLLOOOOOOOOOPPPPPPP", count)
        loop +=1
        priority = heapq.heappop(frontier)  # remove the element with ther highest priority
        # print("PRIORITY = ", priority)
        node = priority[2]
        parent_goals = priority[3]
        # print("LLLLLOOOOOOOOOPPPPPPP", count)
        # parent_goals.sort()
        visit_parent = (node, tuple(parent_goals))
        visited[visit_parent] = priority[1]   # g(x)
        # figure out the order of Ojectives to visit
        # goals = M_of_M(node,goals)
        count += 1
        if maze.isObjective(node[0],node[1]) and len(parent_goals) == 0:
            done = True
            end_state = visit_parent
            # print ("end_state", pred)
            break

        neighbors = maze.getNeighbors(node[0],node[1])
        for i in neighbors:
            child_node = i
            g = priority[1] + 1      # update distance from start
            print("g_val = ", g)
            if maze.isObjective(child_node[0],child_node[1]) and child_node in parent_goals:
                node = child_node       # node == Goal State
                child_goals  = list(parent_goals)
                child_goals.remove(node)      #remove goal from the goals copy list

                child_goals  = tuple(child_goals)
                if child_goals not in goals_MST and len(child_goals) != 0:
                    mst_val = Prim_MST(child_goals)
                    h =  mst_val
                    goals_MST[child_goals] = mst_val
                elif len(child_goals) == 0:
                    h = 0
                else: h = goals_MST[child_goals]
                f = h + g
                visit_child = (child_node, child_goals)  # rebuild the child state
                new_priority = (f, g , child_node, child_goals)

                pred[visit_child] = visit_parent

                start_node = node      # reset the start node to the goal I am at
                if len(child_goals) == 0:
                    done = True
                    end_state = visit_child
                    # print ("end_state", pred)
                    break

            else:
                if parent_goals not in goals_MST :
                    mst_val = Prim_MST(parent_goals)
                    h =  mst_val
                    goals_MST[parent_goals] = mst_val
                else: h = goals_MST[parent_goals]
                f = h + g
                # print("PPPPPPPRRRRRRRIIIIIIMMMMMM", prim_count)
                # prim_count += 1
                child_goals = copy(parent_goals)
                visit_child = (child_node, child_goals)
                new_priority = (f, g , child_node, child_goals)  # (f(x), g(x), child, list goals left)
            print("h_val = ", h)
            if visit_child not in visited and new_priority not in frontier:     # add to frontier if not visited or in priority queue
                    if visit_child not in pred:
                        pred[visit_child] = visit_parent                   # set the predecessor for the neighbor/child
                    heapq.heappush(frontier, new_priority)     # add neighbors to frontier list 

            elif  visit_child in visited and visited[visit_child] >  g:
                    pred[visit_child] = visit_parent                   # set the predecessor for the neighbor/child
                    heapq.heappush(frontier, new_priority)     # add neighbors to frontier list 

        if done:  # All goal states found, so end A* search
            break    

    path = path + backtrack_MST(end_state,pred,maze.getStart(),maze.getObjectives())
    print(path)
    # print(backtracking(end_state,pred,maze.getStart(),maze.getObjectives()))
    # print("valid_path: ",maze.isValidPath(path))

    return path            

def extra(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
