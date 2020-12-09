from typing import List
from collections import deque

import numpy as np


class Preamble:

    def __init__(self, initial_values: List[int]):
        self.deque_previous = deque(initial_values)
        self.accumulated_sum = sum(initial_values)

    def append(self, n):
        self.deque_previous.popleft()
        self.deque_previous.append(n)

    def accumulate(self, n, target_sum):
        self.deque_previous.append(n)
        self.accumulated_sum += n
        while self.accumulated_sum > target_sum:
            self.accumulated_sum -= self.deque_previous.popleft()

    def validate1(self, n):
        return self.is_sum_of_two_previous(n, self.deque_previous)

    @staticmethod
    def is_sum_of_two_previous(n, previous_values):
        for i in range(0, len(previous_values)):
            vi = previous_values[i]
            for j in range(i, len(previous_values)):
                vj = previous_values[j]
                if n == vi + vj:
                    return vi + vj


def get_first_invalid(value_generator, initial_size):
    initial_values = get_initial_values(value_generator, initial_size)
    preamble = Preamble(initial_values)
    for n in value_generator:
        if not preamble.validate1(n):
            return n
        preamble.append(n)
    return -1


def get_sequence_adding_to(value_generator, target_sum):
    initial_values = get_initial_values(value_generator, 1)
    preamble = Preamble(initial_values)
    for n in value_generator:
        preamble.accumulate(n, target_sum)
        if preamble.accumulated_sum == target_sum:
            return min(preamble.deque_previous) + max(preamble.deque_previous)


def get_initial_values(value_generator, initial_size):
    initial_values = []
    for i in range(0, initial_size):
        initial_values.append(next(value_generator))
    return initial_values


def get_value_generator(filename):
    with open(filename) as f:
        for line in f:
            yield int(line)


def part1():
    value_generator = get_value_generator('d9')
    return get_first_invalid(value_generator, 25)


def part2():
    value_generator = get_value_generator('d9')
    return get_sequence_adding_to(value_generator, 14144619)


print(part1())
assert part1() == 14144619

print(part2())
assert part2() == 1766397
