import copy
import random
import numpy as np

from moving_mode_for_different_distance import BullFighter, Bull
from maze_for_robot import Cell
import math

def euclidean_heuristic(cell1: Cell, cell2: Cell):
    x1, y1 = cell1.position
    x2, y2 = cell2.position
    return math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))

def display(maze, bull_position, robot_position):
    # maze[bull_position[0]][bull_position[1]]="B"
    # maze[robot_position[0]][robot_position[1]]="R"
    # print("*")
    print("bull:", bull_position)
    print("robot", robot_position)
    print("***********************")

def test():
    maze=[[0 for i in range(13)] for j in range(13)]
    blocks=[(5,5), (5,7), (6,5), (6,7), (7,5), (7,6), (7,7)]
    for i, j in blocks:
        maze[i][j]=1

    all_position=[]
    for i in range(13):
        for j in range(13):
            if maze[i][j]!=1:
                all_position.append((i,j))

    all_position.remove((6,6))
    all_position.remove((5,6))

    total=[]


    for i in range(10):

        # index1=random.randint(0, len(all_position)-1)
        # index2=index1
        # while index2==index1:
        #     index2=random.randint(0, len(all_position)-1)
        #
        # print(all_position[index1])
        # print(all_position[index2])
        bf=BullFighter((0,0),maze,(6,6),euclidean_heuristic)
        bl=Bull((12,12),maze)

        # bf.simulate_bull_move((6,9),(10,8))

        bf_p = bf.position
        bl_p = bl.position



        count=0
        while True:
            count+=1
            bf_p=bf.move(bl_p)
            bl_p=bl.move(bf_p)
            if bl_p==(6,6):
                break
            display(copy.deepcopy(maze), bl_p, bf_p)
        # print("finish!!!!")
        print(count)
        total.append(count)

    print(np.mean(total))

if __name__ == '__main__':
    test()