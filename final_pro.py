import copy
import random
import numpy as np
from collections import Counter

from moving_mode import BullFighter, Bull
from maze_for_robot import Cell
import math
import time
import json
import os

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

    data={}

    for i in range(5000):
        data[str(i)]={}
        # index1=random.randint(0, len(all_position)-1)
        # index2=index1
        # while index2==index1:
        #     index2=random.randint(0, len(all_position)-1)
        #
        # print(all_position[index1])
        # print(all_position[index2])
        bf=BullFighter((12,12),maze,(6,6),euclidean_heuristic)
        bl=Bull((0,0),maze)

        # bf.simulate_bull_move((6,9),(10,8))

        bf_p = bf.position
        bl_p = bl.position



        count=0
        st = time.time()
        while True:
            count+=1
            bf_p=bf.move(bl_p)
            bl_p=bl.move(bf_p)
            if bl_p==(6,6):
                break
            # display(copy.deepcopy(maze), bl_p, bf_p)
        # print("finish!!!!")
        ed=time.time()-st
        data[str(i)]['len']=count
        data[str(i)]['time']=ed
        print(count)
        a=dict(Counter(bf.strategy))
        print(a)
        if 30>a['gui']>20:
            asd=[]
            for index, bf_path in enumerate(bf.path):
                asd.append([bf_path, bl.path[index]])
            print(asd)
        total.append(count)

    print(np.mean(total))
    current_path=os.path.dirname(os.path.abspath("__file__"))
    save_file=os.path.join(current_path, "data_shy_bull.json")
    data_str=json.dumps(data)
    with open(save_file, 'w') as a:
        a.write(data_str)

if __name__ == '__main__':
    test()
    # current_path = os.path.dirname(os.path.abspath("__file__"))
    # print(current_path)