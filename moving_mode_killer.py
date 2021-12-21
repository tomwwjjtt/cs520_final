from algorithm import AStar
from maze_for_robot import Maze as Maze_robot, Cell
from maze_for_bull import Maze as Maze_bull
import numpy as np
import random


class BullFighter:
    def __init__(self, start_position, maze, x_position, heuristic):
        self.position = start_position
        self.width = len(maze)
        self.height = len(maze[0])
        self.maze_robot = Maze_robot(self.width, self.height)
        self.maze_robot.data = maze
        self.maze_bull = Maze_bull(self.width, self.height)
        self.maze_bull.data = maze
        self.heuristic = heuristic
        self.Astar_robot = AStar(self.maze_robot, heuristic)
        self.Astar_bull = AStar(self.maze_bull, heuristic)
        self.x_position = x_position
        self.surround_target = self.generate_surround_position()

        # for test
        self.path=[]
        self.strategy=[]

    def generate_surround_position(self):
        surround_position = []
        x_x, x_y = self.x_position
        for ox, oy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            surround_position.append((x_x + ox, x_y + oy))
        return surround_position

    def approaching_mode(self, target_position):
        start_cell = Cell(self.position)
        goal_cell = Cell(target_position)
        path = self.Astar_robot.search(start_cell, goal_cell)
        self.position = path[1].get_position()
        if self.position==(5,6):
            self.position=(4,6)
        return self.position

    @staticmethod
    def in_bull_sight(current_position, target_position):
        if abs(current_position[0] - target_position[0]) <= 2 and abs(current_position[1] - target_position[1]) <= 2:
            return True
        else:
            return False

    def is_surround_target(self, robot_position):
        # only one cell surround target
        # if robot_position[0]==self.x_position[0]-1 and robot_position[1]==self.x_position[1]:
        if robot_position==(5, 6):
            return True
        else:
            return False

    @staticmethod
    def not_near_bull(robot_position, bull_position):
        bx, by=bull_position
        for ox,oy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (bx+ox, by+oy)==robot_position:
                return False
        return True

    def get_available_forward(self, target_position):
        available_position = []
        for ox, oy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            cx, cy = self.position
            nx, ny = cx + ox, cy + oy
            if self.maze_robot.position_is_valid(nx, ny) and not self.maze_robot.is_obstacle(nx, ny):
                if not self.is_surround_target((nx, ny)):
                    if self.in_bull_sight([nx, ny], target_position):
                        if self.not_near_bull((nx,ny), target_position):
                            if target_position != (nx, ny):
                                available_position.append((nx, ny))
        return available_position

    def simulate_bull_move(self, robot_position, bull_position):
        total_length = []
        possible_movement = []
        bx, by = bull_position
        current_dist = abs(robot_position[0] - bull_position[0]) + abs(robot_position[1] - bull_position[1])
        for ox, oy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = bx + ox, by + oy
            if self.maze_bull.position_is_valid(nx, ny):
                if nx == robot_position[0] and ny == robot_position[1]:
                    possible_movement.append((bx, by))
                else:
                    if abs(robot_position[0] - nx) + abs(robot_position[1] - ny) <= current_dist:
                        if self.maze_bull.is_obstacle(nx, ny):
                            possible_movement.append((bx, by))
                        else:
                            possible_movement.append((nx, ny))
        for new_position in possible_movement:
            start_cell = Cell(new_position)
            goal_cell = Cell(tuple(self.x_position))
            path = self.Astar_bull.search(start_cell, goal_cell)
            total_length.append(len(path))
        return total_length

    @staticmethod
    def cal_dist(current_position, robot_position):
        return abs(current_position[0] - robot_position[0]) + abs(current_position[1] - robot_position[1])

    def filter_cells(self, available_position):
        filtered_cells=[]
        current_dist=self.cal_dist(self.position, self.x_position)
        for nx, ny in available_position:
            if abs(self.x_position[0]-nx)<= 2 and abs(self.x_position[1]-ny)<=2:
                filtered_cells.append((nx, ny))
            else:
                if self.cal_dist((nx, ny), self.x_position)<=current_dist:
                    filtered_cells.append((nx, ny))
        if len(filtered_cells)==0:
            filtered_cells=available_position
        return filtered_cells

    def navigating_mode(self, target_position):
        available_position = self.get_available_forward(target_position)
        available_position=self.filter_cells(available_position)
        sorted_position = []
        for index, position in enumerate(available_position):
            sorted_position.append((index, np.mean(self.simulate_bull_move(position, target_position))))
        sorted_position.sort(key=lambda t: t[1])
        self.position = available_position[sorted_position[0][0]]
        return self.position

    def guiding_mode(self, bull_position):
        available_position = self.get_available_forward(bull_position)
        sorted_solution = []
        all_possible_solution = []
        available_position.sort(key=lambda t: abs(t[0]-self.x_position[0])+abs(t[1]-self.x_position[1]))
        for position in available_position:
            all_possible_solution.append(self.simulate_bull_move(position, bull_position))
            all_possible_solution[-1].sort()
        for i in range(len(all_possible_solution)):
            sorted_solution.append((i, all_possible_solution[i]))
        sorted_solution.sort(key=lambda t: t[1])
        if len(sorted_solution)==0:
            print("a")
        self.position = available_position[sorted_solution[0][0]]
        return self.position

    def move(self, bull_position):
        # if self.position==(1,6):
        #     print("a")
        if not self.in_bull_sight(self.position, bull_position):
            current_position = self.approaching_mode(bull_position)
            self.strategy.append("app")
        elif self.in_bull_sight(self.position, bull_position) and (abs(self.x_position[0] - bull_position[0])>3 or abs(
                self.x_position[1] - bull_position[1]) >3):
            current_position = self.navigating_mode(bull_position)
            self.strategy.append("nav")
        else:
            current_position = self.guiding_mode(bull_position)
            self.strategy.append("gui")
        self.path.append(current_position)
        return current_position


class Bull:
    def __init__(self, position, maze):
        self.position = position
        self.height = len(maze)
        self.width = len(maze[0])
        self.maze = Maze_bull(self.height, self.width)
        self.maze.data = maze

    def laid_back_mode(self):
        cx, cy = self.position
        next_position = []
        for ox, oy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + ox, cy + oy
            if self.maze.position_is_valid(nx, ny):
                if self.maze.is_obstacle(nx, ny):
                    next_position.append((cx, cy))
                else:
                    next_position.append((nx, ny))
        index = random.randint(0, len(next_position) - 1)
        self.position = next_position[index]
        return self.position

    @staticmethod
    def cal_dist(current_position, robot_position):
        return abs(current_position[0] - robot_position[0]) + abs(current_position[1] - robot_position[1])

    def crash_mode(self, robot_position):
        current_distance = self.cal_dist(self.position, robot_position)
        cx, cy = self.position
        next_position = []
        for ox, oy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + ox, cy + oy
            if self.maze.position_is_valid(nx, ny):
                new_dist = self.cal_dist((nx, ny), robot_position)
                if new_dist <= current_distance:
                    if self.maze.is_obstacle(nx, ny):
                        next_position.append((cx, cy))
                    else:
                        next_position.append((nx, ny))
            # if robot_position[0]==nx and robot_position[1]==ny:
            #     next_position=[(cx, cy)]
            #     break
        if len(next_position)==0:
            print(self.position)
            print(robot_position)
        index = random.randint(0, len(next_position) - 1)
        self.position = next_position[index]
        return self.position

    @staticmethod
    def in_bull_sight(current_position, target_position):
        if abs(current_position[0] - target_position[0]) <= 2 and abs(current_position[1] - target_position[1]) <= 2:
            return True
        else:
            return False

    def move(self, robot_position):
        if self.in_bull_sight(self.position, robot_position):
            current_position = self.crash_mode(robot_position)
        else:
            current_position = self.laid_back_mode()
        return current_position
