import re
from typing import Dict

from utils.files import EmptyLine, read_file

all_passport = ""

re_byr = re.compile('^[0-9]{4}$')
re_iyr = re.compile('^[0-9]{4}$')
re_eyr = re.compile('^[0-9]{4}$')
re_hgt_in = re.compile('^[0-9]+in$')
re_hgt_cm = re.compile('^[0-9]+cm$')
re_hcl = re.compile('^#[0-9a-f]{6}$')
set_ecl = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
re_pid = re.compile('^[0-9]{9}$')


class Passport:
    regex_value = re.compile('[a-z]{3}:[^ \n]+')
    values: Dict

    def __init__(self):
        self.values = dict()

    def add_fields(self, row):
        all_values = re.findall(self.regex_value, row)
        for value in all_values:
            splitted = value.split(':')
            self.values[splitted[0]] = splitted[1]

    def is_valid(self):
        return len(self.values) == 8 or (len(self.values) == 7 and 'cid' not in self.values)

    def is_valid2(self):

        if not self.is_valid():
            return False

        byr = self.values.get('byr', None)
        if not byr or not re.match(re_byr, byr) or not 1920 <= int(byr) <= 2002:
            return False

        iyr = self.values.get('iyr', None)
        if not iyr or not re.match(re_iyr, iyr) or not 2010 <= int(iyr) <= 2020:
            return False

        eyr = self.values.get('eyr', None)
        if not eyr or not re.match(re_eyr, eyr) or not 2020 <= int(eyr) <= 2030:
            return False

        hgt = self.values.get('hgt', None)
        if not hgt or (not re.match(re_hgt_cm, hgt) and not re.match(re_hgt_in, hgt)):
            return False
        if re.match(re_hgt_cm, hgt) and not 150 <= int(hgt[:-2]) <= 193:
            return False
        if re.match(re_hgt_in, hgt) and not 59 <= int(hgt[:-2]) <= 76:
            return False

        hcl = self.values.get('hcl', None)
        if not hcl or not re.match(re_hcl, hcl):
            return False

        ecl = self.values.get('ecl', None)
        if not hcl or ecl not in set_ecl:
            return False

        pid = self.values.get('pid', None)
        if not pid or not re.match(re_pid, pid):
            return False

        return True

    def __str__(self):
        return str(self.values)


def passports(filename):
    passport = Passport()
    with read_file(filename) as f:
        for row in f:
            if row is not EmptyLine:
                passport.add_fields(row)
            else:
                yield passport
                passport = Passport()
    yield passport


def part1():
    count_valid = 0
    for passport in passports('d4'):
        if passport.is_valid():
            count_valid += 1
    return count_valid


def part2():
    count_valid = 0
    for passport in passports('d4'):
        if passport.is_valid2():
            count_valid += 1
    return count_valid


print(part1())
print(part2())

assert part1() == 245
assert part2() == 133
