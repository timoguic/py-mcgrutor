""" Module to generate random maze """

from random import randint
import numpy

# Thank you, Wikipedia
# https://en.wikipedia.org/wiki/Maze_generation_algorithm#Python_code_example


def maze(width=81, height=51, complexity=0.75, density=0.75):
    """ Generates random maze """

    # Only odd shapes
    shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))  # number of components
    density = int(density * ((shape[0] // 2) * (shape[1] // 2)))  # size of components
    # Build actual maze
    Z = numpy.zeros(shape, dtype=bool)
    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make aisles
    for i in range(density):
        x, y = (
            randint(0, shape[1] // 2) * 2,
            randint(0, shape[0] // 2) * 2,
        )  # pick a random position
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:
                neighbours.append((y, x - 2))
            if x < shape[1] - 2:
                neighbours.append((y, x + 2))
            if y > 1:
                neighbours.append((y - 2, x))
            if y < shape[0] - 2:
                neighbours.append((y + 2, x))
            if len(neighbours):
                y_, x_ = neighbours[randint(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_

    return [["|" if i else " " for i in l] for l in Z.tolist()]


if __name__ == "__main__":
    print(maze(15, 15))
