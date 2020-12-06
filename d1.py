import utils

all_values = [int(r) for r in open('d1')]
target_sum = 2020


def aggregate(deepness, start_index=None, current_sum=0):
    new_sum = current_sum
    if start_index is not None:
        current_value = all_values[start_index]
        new_sum = current_sum + current_value
        if new_sum > target_sum:
            return None
        if not deepness and new_sum == target_sum:
            return []
        if not deepness:
            return None
    start_iteration_at = 0 if start_index is None else start_index + 1

    for idx in range(start_iteration_at, len(all_values)):
        result_indices = aggregate(deepness - 1, idx, new_sum)
        if result_indices is not None:
            return [idx, *result_indices]


def part1():
    indices = aggregate(2)
    return utils.prod([all_values[i] for i in indices])


def part2():
    indices = aggregate(3)
    return utils.prod([all_values[i] for i in indices])


print(part1())
print(part2())

assert part1() == 1016619
assert part2() == 218767230
