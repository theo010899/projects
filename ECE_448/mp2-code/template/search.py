# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush

def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)

def bfs(maze):
    # Write your code here
    """
    This function returns optimal path in a list, which contains start and objective.
    If no path found, return None. 
    """
    # print("MAZE", maze)
    node = maze.getStart()
    if maze.isObjective(node[0],node[1],node[2]):
        solution = [node]
        return solution


    # create traversal queue
    bfs_Q = []
    # create a visited list
    visited = set()
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
    # print("START_VAL",node)

    # BFS loop
    while len(bfs_Q) != 0:      # while the traversal list is not empty     and maze.isObjective(node[0],node[1]) == False
        node = bfs_Q[0]         # load the first element into the current node
        del bfs_Q[0]            # pop off the first element in the list
        visited.add(node)
        # print("CUR_NODE",node)
        for i in maze.getNeighbors(node[0],node[1], node[2]):  # get the neighbors of node
            child_node = i
            # print("CHILD", child_node)
            # print("Parent", node)
            if child_node not in visited and child_node not in bfs_Q:
                if maze.isObjective(child_node[0],child_node[1], child_node[2]):     #check if it is the goal state
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
        return None  

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
    print(path)
    return path

