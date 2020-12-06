import functools


def bin_to_dec(binary: str):
    return int(bytes(binary, 'utf8'), 2)


def to_row(encoded_row: str):
    encoded_row = encoded_row.replace('F', '0')
    encoded_row = encoded_row.replace('B', '1')
    return bin_to_dec(encoded_row)


def to_column(encode_col: str):
    encode_col = encode_col.replace('L', '0')
    encode_col = encode_col.replace('R', '1')
    return bin_to_dec(encode_col)


def to_index(encode_seat: str):
    return 8 * to_row(encode_seat[0:7]) + to_column(encode_seat[7:])


def max_index(previous_max, row):
    return max(previous_max, to_index(row))


def part1():
    return functools.reduce(max_index, open('d5'), -1)


def part2():
    all_idx = set([to_index(s) for s in open('d5')])
    for i in range(0, 127 * 8):
        if i - 1 in all_idx and i + 1 in all_idx and i not in all_idx:
            return i


print(part1())
print(part2())

assert part1() == 980
assert part2() == 607
