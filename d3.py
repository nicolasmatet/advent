import math

all_rows = [r for r in open('d3')]
trees_width = 31


def is_tree(row, pos):
    return row[pos] == '#'


def get_tree_count(right, down):
    count_trees = 0
    pos = 0
    for row_idx in range(0, len(all_rows), down):
        row = all_rows[row_idx]
        if is_tree(row, pos):
            count_trees += 1
        pos = (pos + right) % trees_width
    return count_trees


def part1():
    return get_tree_count(3, 1)


def part2():
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    all_count = [get_tree_count(*slope) for slope in slopes]
    return math.prod(all_count)


print(part1())
print(part2())

assert part1() == 270
assert part2() == 2122848000
