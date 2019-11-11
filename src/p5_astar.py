from p5 import *
import matplotlib.pyplot as plt
import numpy as np
import math

class Node():
    def __init__(self, parent, position):
        self.previous = parent
        self.position = position
        self.neighbors = []
        self.f = 0
        self.g = 0
        self.h = 0
        self.wall = 0

    def show(self, color):
        global w, h
        background(0)
        stroke(0)
        if self.wall != 1:
            fill(color[0], color[1], color[2])
        else:
            fill(0, 0, 0)
        rect((self.position[0]*w, self.position[1]*h), w, h)

    def addNeighbors(self, grid):
        x = self.position[0]
        y = self.position[1]
        if x < cols - 1:
            self.neighbors.append(grid[x + 1, y])
        if x > 0:
            self.neighbors.append(grid[x - 1, y])
        if y < rows - 1:
            self.neighbors.append(grid[x, y + 1])
        if y > 0:
            self.neighbors.append(grid[x, y - 1])
        if (x > 0) and (y > 0):
            self.neighbors.append(grid[x - 1, y - 1])
        if (x > cols -1) and (y > 0):
            self.neighbors.append(grid[x + 1, y - 1])
        if (x > 0) and (y < rows - 1):
            self.neighbors.append(grid[x - 1, y + 1])
        if (x < cols - 1) and (y < rows - 1):
            self.neighbors.append(grid[x + 1, y + 1])

cols = 10
rows = 10
w = 0
h = 0
start = None
end = None
grid = np.empty((rows, cols), dtype=Node)
open_list = []
closed_list = []
path = []

def removeFromArray(array, elem):
    i = len(array) - 1
    while i >= 0:
        if array[i] == elem:
            del array[i]
            break
        i -= 1

def heuristic(a, b):
    d = math.sqrt(((b.position[0] - a.position[0]) ** 2) + ((b.position[1] - a.position[1]) ** 2))
    return d

def setup():
    global grid, open_list, closed_list, w, h, start, end
    size(640, 640)

    w = 640 / cols
    h = 640 / rows

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            grid[i, j] = Node(None, [i, j])

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            grid[i, j].addNeighbors(grid)

    wall1 = [[4,7],[5,7],[6,7],[7,7]]
    wall1 = np.reshape(wall1, (4, 2))
    wall2 = np.flip(wall1, 1)

    wall1_count = 0
    wall2_count = 0

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if wall1_count <= 3:
                if i == wall1[wall1_count, 0] and j == wall1[wall1_count, 1]:
                    grid[i, j].wall = 1
                    wall1_count += 1
            if wall2_count <= 3:
                if i == wall2[wall2_count, 0] and j == wall2[wall2_count, 1]:
                    grid[i, j].wall = 1
                    wall2_count += 1

    start = grid[0, 0]
    end = grid[9, 9]

    # wall1 = [[20,30],[21,30],[22,30],[23,30],[24,30],[25,30],[26,30],[27,30],[28,30],[29,30],[30,30]]
    # wall1 = np.reshape(wall1, (11, 2))
    # wall2 = np.flip(wall1, 1)
    #
    # wall1_count = 0
    # wall2_count = 0
    #
    # for i in range(grid.shape[0]):
    #     for j in range(grid.shape[1]):
    #         if wall1_count <= 10:
    #             if i == wall1[wall1_count, 0] and j == wall1[wall1_count, 1]:
    #                 grid[i, j].wall = 1
    #                 wall1_count += 1
    #         if wall2_count <= 10:
    #             if i == wall2[wall2_count, 0] and j == wall2[wall2_count, 1]:
    #                 grid[i, j].wall = 1
    #                 wall2_count += 1
    #
    # start = grid[0, 0]
    # end = grid[35, 35]
    open_list.append(start)

def draw():
    global grid, open_list, closed_list, start, end, path
    #A* algorithm
    if len(open_list) > 0:
        winner = 0
        for i in range(len(open_list)):
            if open_list[i].f < open_list[winner].f:
                winner = i

        current = open_list[winner]
        if current == end:
            no_loop()
            print("done")
            return

        removeFromArray(open_list, current)
        closed_list.append(current)

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            temp_g = 0
            if not neighbor in closed_list and neighbor.wall != 1:
                temp_g = current.g + 1

                new_path = 0
                if neighbor in open_list:
                    if temp_g < neighbor.g:
                        neighbor.g = temp_g
                        new_path = 1
                else:
                    neighbor.g = temp_g
                    new_path = 1
                    open_list.append(neighbor)

                if new_path == 1:
                    neighbor.h = heuristic(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous = current
    else:
        print("no solution")

    #draw figure
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            grid[i][j].show([255, 255, 255])

    for node in closed_list:
        node.show([255, 0, 0])

    for node in open_list:
        node.show([0, 0, 255])

    temp = current
    path = []
    while temp.previous:
        path.append(temp.previous)
        temp = temp.previous

    for i in range(len(path)):
        path[i].show([0, 255, 0])
run()