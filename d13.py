import re
from math import prod

import numpy as np

regex_id = re.compile('[0-9]+')


def parse_schedule(filename):
    with open(filename) as schedule:
        lines = schedule.readlines()
        earliest_time = int(lines[0].strip())
        buses_ids = [int(bus_id) for bus_id in re.findall(regex_id, lines[1])]
        return earliest_time, buses_ids


def parse_offset(filename):
    list_ids, list_offsets = [], []

    with open(filename) as schedule:
        lines = schedule.readlines()
        bus_ids = lines[1].strip().split(',')
        for offset, bus_id in enumerate(bus_ids):
            if bus_id != 'x':
                list_ids.append(int(bus_id))
                list_offsets.append(offset)
        return list_ids, list_offsets


def bezout(a, b):
    if b == 0:
        return 1, 0
    u, v = bezout(b, a % b)
    return v, u - (a // b) * v


def get_n_tidle(list_ns, i):
    if i == 0:
        return prod(list_ns[1:])
    if i == len(list_ns) - 1:
        return prod(list_ns[:-1])
    return prod(list_ns[:i]) * prod(list_ns[i + 1:])


def part1(filename):
    earliest_time, bus_ids = parse_schedule(filename)
    waiting_times = [((earliest_time // bus_id) + 1) * bus_id - earliest_time for bus_id in bus_ids]
    idx_max = np.argmin(waiting_times)
    return waiting_times[idx_max] * bus_ids[idx_max]


def part2(filename):
    list_ids, list_offsets = parse_offset(filename)
    n_tidles = [get_n_tidle(list_ids, i) for i in range(0, len(list_ids))]
    bezouts = [bezout(n_tidle, n) for n_tidle, n in zip(n_tidles, list_ids)]
    earliest = sum(
        [- offset * bezout_coeff[0] * n_tidle
         for offset, bezout_coeff, n_tidle
         in zip(list_offsets, bezouts, n_tidles)])
    if earliest < 0:
        pcm = prod(list_ids)
        earliest = earliest + (abs(earliest) // pcm + 1) * pcm
    return earliest


print(part1('d13'))
assert part1('d13') == 2298
print(part2('d13'))
assert(part2('d13') == 783685719679632)
