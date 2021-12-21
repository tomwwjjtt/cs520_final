import math
import queue
from maze_for_robot import Cell, Maze


class AStar:
    def __init__(self, maze: Maze, heuristic):
        '''
        maze: from maze_for_robot.py
        '''
        self.maze = maze
        self.heuristic = heuristic

    def search(self, start_cell: Cell, goal_cell: Cell):
        # user a priority queue, always select the cell with smallest fn to explore
        open_list = queue.PriorityQueue()
        start_cell.set_father_node(None)
        # calculate fn and hn
        start_cell.update_fn(self.heuristic, goal_cell)

        open_list.put((start_cell.fn, start_cell))  # (fn, Cell)
        closed_dict = dict()  # cells already visited, {Cell : gn}
        while not open_list.empty():
            fn, current_cell = open_list.get()
            # reach the goal cell
            if current_cell.get_position() == goal_cell.get_position():
                return self.get_path(current_cell)
            # the current cell has been visited
            if current_cell in closed_dict:
                continue
            closed_dict[current_cell] = current_cell.gn
            # Generate the children of n (neighbors believed or known to be unoccupied)
            for child_cell in self.maze.generate_children(current_cell, goal_cell):
                # update hn and fn of child cell
                child_cell.update_fn(self.heuristic, goal_cell)
                '''
                The successors of n are the children n0 that are newly discovered, or g(n0) > g(n) + 1.
                For each successor n0, re-set g(n0) = g(n) + 1, representing the newly discovered shortest path from the start node to n0 newly discovered, insert n0 into the fringe at priority f(n0) = g(n0) + h(n0)
                '''
                if child_cell not in closed_dict:
                    open_list.put((child_cell.fn, child_cell))
                # g(n0) > g(n) + 1, insert n0 into the fringe at priority f(n0) = g(n0) + h(n0),
                elif child_cell.gn < closed_dict[child_cell]:
                    closed_dict.pop(child_cell)
                    open_list.put((child_cell.fn, child_cell))
        # no path found
        return []

    def get_path(self, current_cell: Cell):
        '''
        Get the path, search from current cell to start cell
        '''
        path = []
        # starts from the goal and go back to the start cell
        while current_cell is not None:
            path.append(current_cell)
            current_cell = current_cell.father_node
        return path[::-1]


