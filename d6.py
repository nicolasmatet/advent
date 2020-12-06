import functools
from collections import defaultdict
from typing import Set, Dict

from utils.files import read_file, EmptyLine


class GroupAnswers:
    uniqueAnswers: Dict
    members: int

    def __init__(self):
        self.members = 0
        self.uniqueAnswers = defaultdict(lambda: 0)

    def add_answers(self, row):
        self.members += 1
        for a in row:
            self.uniqueAnswers[a] += 1

    def count(self):
        return len(self.uniqueAnswers)

    def count2(self):
        return len([a for a, c in self.uniqueAnswers.items() if c == self.members])


def all_group_answers(filename):
    group_answers = GroupAnswers()
    with read_file(filename) as f:
        for row in f:
            if row is not EmptyLine:
                group_answers.add_answers(row)
            else:
                yield group_answers
                group_answers = GroupAnswers()
    yield group_answers


def sum_group_answers1(previous_count, group_answers):
    return previous_count + group_answers.count()


def sum_group_answers2(previous_count, group_answers):
    return previous_count + group_answers.count2()


def part1():
    return functools.reduce(sum_group_answers1, all_group_answers('d6'), 0)


def part2():
    return functools.reduce(sum_group_answers2, all_group_answers('d6'), 0)


print(part1())
print(part2())

assert part1() == 6735
assert part2() == 3221
