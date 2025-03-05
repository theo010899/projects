# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position (int,int):of the arm link, (x-coordinate, y-coordinate)
    """

    start_X = start[0]

    start_Y = start[1]

    # ang_in_rad  = math.radians(angle)

    Y_len = int(length * math.sin(math.radians(angle)))

    X_len = int(length * math.cos(math.radians(angle)))

    end_X =  start_X + X_len

    end_Y = start_Y - Y_len 

    return (end_X, end_Y)

def doesArmTouchObjects(armPosDist, objects, isGoal=False):
    """Determine whether the given arm links touch any obstacle or goal

        Args:
            armPosDist (list): start and end position and padding distance of all arm links [(start, end, distance)]
            objects (list): x-, y- coordinate and radius of object (obstacles or goals) [(x, y, r)]
            isGoal (bool): True if the object is a goal and False if the object is an obstacle.
                           When the object is an obstacle, consider padding distance.
                           When the object is a goal, no need to consider padding distance.
        Return:
            True if touched. False if not.
    """

    for link in armPosDist:
       p1 = link[0]  # link start point A
       p2 = link[1]  # link end point B

       for obj in objects:
           p0 = (obj[0],obj[1])  # obstacle point C

        #    print("P_0", p0, "P_1", p1, "P_2", p2)


        #    term_0 = (p2[0]-p1[0]) * (p2[0]-p1[0])

        #    term_1 = (p2[1]-p1[1]) * (p2[1]-p1[1])

        #    side_AB = (term_0 + term_1)**.5  # AB distance

        #    term_2 = (p0[0]-p1[0]) * (p0[0]-p1[0])

        #    term_3 = (p0[1]-p1[1]) * (p0[1]-p1[1])

        #    side_AC = ( term_2 + term_3)**.5  # AC distance

        #    term_4 = (p2[0]-p0[0]) *(p2[0]-p0[0]) 

        #    term_5 = (p2[1]-p0[1]) * (p2[1]-p0[1])

        #    side_BC = (term_4 + term_5 )**.5   # BC distance

           run_AC = (p0[0]-p1[0])

           run_BC = (p0[0]-p2[0]) 

           px = p2[0] - p1[0]
           py = p2[1] - p1[1]
           norm = px*px + py*py
           num = ((p0[0]-p1[0])*px + (p0[1]-p1[1])*py)/float(norm)

           if num  > 1:
                num = 1
           elif num < 0:
                num = 0

           x = p1[0] + num * px
           y = p1[1] + num * py

           dx = x - p0[0]
           dy = y - p0[1]

           dist = (dx*dx + dy*dy)**.5

           if run_AC <= 0:              # math.degrees(theta1) > 90:
            #    print("HELLO", side_AC - link[2], "  ", obj[2] )
               if isGoal == False:
                    if dist <= obj[2]  + link[2]:
                        return True
               else:
                    if dist <= obj[2]:
                        return True
           elif run_BC >= 0:
                if isGoal == False:
                    if dist  <= obj[2] + link[2]:
                        return True
                else:
                    if dist <= obj[2]:
                        return True
           else:
                # print("HELLO")
                # num = abs(((p2[1]-p1[1])*p0[0]) - ((p2[0]-p1[0])*p0[1]) + (p2[0]*p1[1]) - (p2[1]*p1[0]))
                # denom = side_AB
                


                if isGoal == False:
                    # dist = (num/denom)    # account for the padding distance
                    # print(dist, "  ", obj[2])
                    if dist <= obj[2] + link[2]:
                        return True
                else:
                    # print("GOODBYE")
                    # dist = (num/denom)    # account for the padding distance
                    # print(dist, "  ", obj[2])
                    if dist <= obj[2]:
                        return True

    return False

def doesArmTipTouchGoals(armEnd, goals):
    """Determine whether the given arm tick touch goals

        Args:
            armEnd (tuple): the arm tick position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]. There can be more than one goal.
        Return:
            True if arm tip touches any goal. False if not.
    """
    for goal in goals:

           term_0 = (goal[0]-armEnd[0]) * (goal[0]-armEnd[0])

           term_1 = (goal[1]-armEnd[1]) * (goal[1]-armEnd[1])

           side_AB = math.sqrt(term_0 + term_1)  # AB distance

           if side_AB <= goal[2]:
               return True

    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end positions of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False if not.
    """

    for link in armPos:
        start = link[0]
        start_X = start[0]
        start_Y = start[1]
        end = link[1]
        end_X = end[0]
        end_Y = end[1]

        if start_X < 0 or start_X > window[0]:
            return False
        if start_Y < 0 or start_Y > window[1]:
            return False
        if end_X < 0 or end_X > window[0]:
            return False
        if end_Y < 0 or end_Y > window[1]:
            return False



    return True


if __name__ == '__main__':
    computeCoordinateParameters = [((150, 190),100,20), ((150, 190),100,40), ((150, 190),100,60), ((150, 190),100,160)]
    resultComputeCoordinate = [(243, 156), (226, 126), (200, 104), (57, 156)]
    testRestuls = [computeCoordinate(start, length, angle) for start, length, angle in computeCoordinateParameters]

    assert testRestuls == resultComputeCoordinate

    testArmPosDists = [((100,100), (135, 110), 4), ((135, 110), (150, 150), 5)]
    testObstacles = [[(120, 100, 5)], [(110, 110, 20)], [(160, 160, 5)], [(130, 105, 10)]]
    resultDoesArmTouchObjects = [
        True, True, False, True, False, True, False, True,
        False, True, False, True, False, False, False, True
    ]

    testResults = []
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle))
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle))

    print("\n")
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))
    # print("             testResults" , testResults, "\nresultDoesArmTouchObjects", resultDoesArmTouchObjects)
    assert resultDoesArmTouchObjects == testResults

    testArmEnds = [(100, 100), (95, 95), (90, 90)]
    testGoal = [(100, 100, 10)]
    resultDoesArmTouchGoals = [True, True, False]

    testResults = [doesArmTipTouchGoals(testArmEnd, testGoal) for testArmEnd in testArmEnds]
    assert resultDoesArmTouchGoals == testResults

    testArmPoss = [((100,100), (135, 110)), ((135, 110), (150, 150))]
    testWindows = [(160, 130), (130, 170), (200, 200)]
    resultIsArmWithinWindow = [True, False, True, False, False, True]
    testResults = []
    for testArmPos in testArmPoss:
        for testWindow in testWindows:
            testResults.append(isArmWithinWindow([testArmPos], testWindow))
    assert resultIsArmWithinWindow == testResults

    print("Test passed\n")
