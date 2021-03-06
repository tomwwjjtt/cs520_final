import random

OBSTACLE = 1
START = 0
GOAL = 0

class Cell:
    def __init__(self, position: tuple, father_node=None):  # position = (x,y)
        self.position = position
        self.father_node = father_node
        self.gn = 0 if father_node is None else self.father_node.get_gn() + 1
        self.hn = None
        self.fn = None

    def get_position(self):
        return self.position

    def set_father_node(self, father):
        self.father_node = father

    def get_father_node(self):
        # change current node to father node
        return self.father_node

    def update_fn(self, heuristic, goal_cell: 'Cell'):
        self.hn = heuristic(self, goal_cell)
        self.fn = self.gn + self.hn

    def get_hn(self):
        '''
        the heuristic value, estimating the distance from the cell n to the goal node
        '''
        return self.hn

    def get_gn(self):
        '''
        this represents the length of the shortest path discovered from the initial search point to cell n so far
        '''
        return self.gn

    def get_fn(self):
        '''
        f(n) is defined to be g(n) + h(n), which estimates the distance from the initial search node to the final goal node through cell n
        '''
        return self.fn

    def __hash__(self):
        return hash(tuple(self.position))

    def __lt__(self, other):
        return self.position < other.position

    def __str__(self):
        return 'Cell({})'.format(self.position)

    def __repr__(self):
        return str(self)

    def __eq__(self, other: "Cell"):
        return tuple(self.position) == tuple(other.position)


class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.data = [[0 for i in range(width)] for j in range(height)]

    def initialize_maze(self, probability: float, random_seed=None):
        '''
        Initialize maze according to the density P∈(0, 0.33)
        When random_seed has been set, the maze will not change
        '''
        if random_seed:
            random.seed(random_seed)
        for i in range(self.height):
            for j in range(self.width):
                # the upper-left and lower-right corner
                if (i, j) == (0, 0):
                    self.data[i][j] = START
                elif (i, j) == (self.height - 1, self.width - 1):
                    self.data[i][j] = GOAL
                # generate obstacle
                elif random.random() <= probability:
                    self.data[i][j] = OBSTACLE

    def maze_show(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.data[i][j], end='')
            print()

    #     def obstacle
    #     def set_maze_obstacles
    #     def draw_start
    #     def draw_goal

    def position_is_valid(self, index_x, index_y):
        '''
        Check if the position (i, j) is valid, an valid position means it's in the maze that are not out of bound of the world
        '''
        return 0 <= index_x < self.height and 0 <= index_y < self.width

    def set_obstacle(self, i, j):
        '''
        Set obstacles with 1
        '''
        self.data[i][j] = 1

    def is_obstacle(self, i, j):
        '''
        Check if the position (i, j) is an obstacle
        '''
        return self.data[i][j] == 1

    def generate_children(self, cell: Cell, goal_cell: Cell):
        '''
        Generate the children of n (neighbors believed or known to be unoccupied)
        '''
        dij = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        children_list = []
        # get current location, and trying to explore the adjacent cells
        i, j = cell.get_position()
        for di, dj in dij:
            ni, nj = i + di, j + dj
            # the position is valid and it's not an obstacle
            if self.position_is_valid(ni, nj) and not self.is_obstacle(ni, nj):
                child = Cell((ni, nj), cell)   # set the father node simultaneously
                children_list.append(child)
        return children_list
