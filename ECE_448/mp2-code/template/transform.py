
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    angles = arm.getArmAngle()
    arm_limits = arm.getArmLimit()

    alpha = angles[0]
    alpha_lim = arm_limits[0]
    num_rows = 1+ int(((alpha_lim[1] - alpha_lim[0])/granularity))

    beta = angles[1]
    beta_lim = arm_limits[1]
    num_cols = 1+ int(((beta_lim[1] - beta_lim[0])/granularity))

    gamma = angles[2]
    gamma_lim = arm_limits[2]
    num_heights = 1+ int(((gamma_lim[1] - gamma_lim[0])/granularity))
    print("num_rows = ", num_rows, "num_heights = ", num_heights, "num_cols = ", num_cols)

    # startpoint = (alpha, beta)    

    offsets = [alpha_lim[0],beta_lim[0],gamma_lim[0]]  #set the offset

    maze = [[[SPACE_CHAR for i in range(num_heights)] for j in range(num_cols)] for k in range(num_rows)]  # intialize input_map
    # print("maze[row][col] = ", maze[0], " ", len(maze))
 
    for row in range(num_rows):
        

        for col in range(num_cols):


            for height in range(num_heights):
                # print("X = ", row, " Y = ", col, " Z = ", height)
                # print("maze_x_size = ", len(maze), "maze_y_size = ", len(maze[0]), "maze_z_size = ", len(maze[0][0]))
                # print("maze[row][col][height] = ", maze[row][col], " ", len(maze[row][col]))
                new_ang = idxToAngle((row,col,height), offsets, granularity)
                # print("NEW_ANGLE = ", new_ang)
                arm.setArmAngle((new_ang[0],new_ang[1], new_ang[2]))

                if doesArmTouchObjects(arm.getArmPosDist(), obstacles, False) or not isArmWithinWindow(arm.getArmPos(), window):
                    maze[row][col][height] = WALL_CHAR
                elif not isArmWithinWindow(arm.getArmPos(), window):
                    maze[row][col][height] = WALL_CHAR
                elif not doesArmTipTouchGoals(arm.getEnd(), goals) and doesArmTouchObjects(arm.getArmPosDist(), goals, True):
                    maze[row][col][height] = WALL_CHAR
                elif doesArmTipTouchGoals(arm.getEnd(), goals):
                    maze[row][col][height] = OBJECTIVE_CHAR


    # print("HELLO")
    start_idx = angleToIdx((alpha,beta, gamma), offsets, granularity)
    maze[start_idx[0]][start_idx[1]][start_idx[2]]  = START_CHAR  # set the start character
    
    return Maze(maze, offsets, granularity)