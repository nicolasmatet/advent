import re


class Password:
    mini: int
    maxi: int
    letter: str
    password: str
    regex_db_row = re.compile('([0-9]+-[0-9]+) ([a-z]{1}): ([a-z]+)')

    def __init__(self, db_row):
        rule, letter, password = re.match(self.regex_db_row, db_row).groups()
        self.letter = letter
        self.mini, self.maxi = self.get_min_max(rule)
        self.password = password

    def get_min_max(self, rule):
        splitted_rule = rule.split('-')
        return int(splitted_rule[0]), int(splitted_rule[1])

    def is_valid(self):
        return self.mini <= self.password.count(self.letter) <= self.maxi

    def is_valid2(self):
        first_letter_ok = self.password[self.mini - 1] == self.letter
        second_letter_ok = self.password[self.maxi - 1] == self.letter
        return first_letter_ok ^ second_letter_ok


assert Password('1-3 a: abcde').is_valid()
assert not Password('1-3 b: cdefg').is_valid()
assert Password('2-9 c: ccccccccc').is_valid()


def part1():
    valid_count = 0
    for password in open('d2'):
        if Password(password).is_valid():
            valid_count += 1
    return valid_count


def part2():
    valid_count = 0
    for password in open('d2'):
        if Password(password).is_valid2():
            valid_count += 1
    return valid_count


print(part1())
print(part2())

assert part1() == 538
assert part2() == 489
