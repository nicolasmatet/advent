import enum
from typing import List
import networkx as nx
import numpy as np

from utils.files import read_file


def matprint(mat, fmt="g"):
    col_maxes = [max([len(("{:" + fmt + "}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:" + str(col_maxes[i]) + fmt + "}").format(y), end="  ")
        print("")


class SeatState(enum.Enum):
    EMPTY = 'L'
    FLOOR = '.'
    OCCUPIED = '#'


def increment_occupied(seat_state):
    if seat_state == SeatState.OCCUPIED.value:
        return 1
    return 0


def get_neigbours_2(row, col, seating):
    neighbors = []
    height, width = seating.shape
    for c in range(col + 1, width):
        seat_state = seating[row, c]
        if seat_state != SeatState.FLOOR.value:
            neighbors.append((row, c))
            break
    for c in range(col - 1, -1, -1):
        seat_state = seating[row, c]
        if seat_state != SeatState.FLOOR.value:
            neighbors.append((row, c))
            break

    for r in range(row - 1, -1, -1):
        seat_state = seating[r, col]
        if seat_state != SeatState.FLOOR.value:
            neighbors.append((r, col))
            break
    for r in range(row + 1, height):
        seat_state = seating[r, col]
        if seat_state != SeatState.FLOOR.value:
            neighbors.append((r, col))
            break

    ## diag
    # ++
    for inc in range(1, height + width):
        r = row + inc
        c = col + inc
        if r >= height or c >= width:
            break
        seat_state = seating[r, c]
        if seat_state != SeatState.FLOOR.value:
            neighbors.append((r, c))
            break

    # + -
    for inc in range(1, height + width):
        r = row + inc
        c = col - inc
        if r >= height or c < 0:
            break
        seat_state = seating[r, c]
        if seat_state != SeatState.FLOOR.value:
            neighbors.append((r, c))
            break

    # - -
    for inc in range(1, height + width):
        r = row - inc
        c = col - inc
        if r < 0 or c < 0:
            break
        seat_state = seating[r, c]
        if seat_state != SeatState.FLOOR.value:
            neighbors.append((r, c))
            break

    # - +
    for inc in range(1, height + width):
        r = row - inc
        c = col + inc
        if r < 0 or c >= width:
            break
        seat_state = seating[r, c]
        if seat_state != SeatState.FLOOR.value:
            neighbors.append((r, c))
            break

    return neighbors


def get_neigbours(row, col, seating):
    neighbors = []
    height, width = seating.shape
    for row_neighbor in range(row - 1, row + 2):
        if Seating.out_of_range(row_neighbor, height):
            continue
        for col_neighbor in range(col - 1, col + 2):
            if Seating.out_of_range(col_neighbor, width):
                continue
            if row_neighbor == row and col_neighbor == col:
                continue
            if seating[row_neighbor, col_neighbor] != SeatState.FLOOR.value:
                neighbors.append((row_neighbor, col_neighbor))
    return neighbors


class Seating:
    def __init__(self, seating: List[List[str]], get_neigbours, threshold_occupied_neighbors=4):
        self.get_neigbours = get_neigbours
        self.threshold_occupied_neighbors = threshold_occupied_neighbors
        self.seating = np.array(seating)
        self.height, self.width = self.seating.shape
        self.g: nx.DiGraph
        self.build_seat_network()
        self.floors = self.seating == SeatState.FLOOR.value

    def __str__(self):
        return str(self.seating)

    def build_seat_network(self):
        self.g = nx.Graph()
        for x in range(0, self.width):
            for y in range(0, self.height):
                neighbors = self.get_neigbours(x, y, self.seating)
                self.g.add_edges_from([((x, y), neighbor) for neighbor in neighbors])

    def get_occupied_neighbors_count(self):
        neighbor_count = np.zeros(shape=self.seating.shape)
        for node in self.g.nodes:
            print([n for n in self.g.neighbors(node)])
            for neighbor in self.g.neighbors(node):
                if self.seating[neighbor[0], neighbor[1]] == SeatState.OCCUPIED.value:
                    neighbor_count[neighbor[0], neighbor[1]] += 1
        return neighbor_count

    def next_step(self):
        neighbors_count = self.get_occupied_neighbors_count()
        matprint(neighbors_count, fmt='')
        become_occupied = (neighbors_count == 0) & ~self.floors
        become_empty = (neighbors_count >= self.threshold_occupied_neighbors) & ~self.floors
        self.seating[become_occupied] = SeatState.OCCUPIED.value
        self.seating[become_empty] = SeatState.EMPTY.value
        has_changed = np.any(become_empty) or np.any(become_occupied)
        return has_changed

    @staticmethod
    def out_of_range(col_or_row, maxi):
        return col_or_row < 0 or col_or_row >= maxi

    def count_occupied(self):
        return np.count_nonzero(self.seating == SeatState.OCCUPIED.value)


def load_seating(filename, get_occupied_neigbours, **kwargs):
    with open(filename) as f:
        lines = f.readlines()
        return Seating([[c for c in line.strip()] for line in lines], get_occupied_neigbours, **kwargs)


def part1(filename):
    seating = load_seating(filename, get_neigbours)
    steps = 0

    print(steps, "************************")
    matprint(seating.seating, fmt='')

    while seating.next_step():
        steps += 1
        print(steps, "************************")
        print(seating.seating)
        # matprint(seating.seating, fmt='')
    return seating.count_occupied()


def part2(filename):
    seating = load_seating(filename, get_neigbours_2, threshold_occupied_neighbors=5)
    steps = 0

    print(steps, "************************")
    # matprint(seating.seating, fmt='')
    while seating.next_step():
        steps += 1
        print(steps, "************************")
        matprint(seating.seating, fmt='')

    return seating.count_occupied()


part1 = part1('d11')
print(part1)
assert part1 == 2481
# print(part2('d11'))
