sin_table = [0, 1, 0, -1]


def sinus(angle):
    return sin_table[(angle // 90) % 4]


def cosinus(angle):
    return sin_table[(angle // 90 + 1) % 4]


def norm0(x, y):
    return abs(x) + abs(y)


def rotate(vector, cos_term, sin_term):
    new_x = cos_term * vector[0] - sin_term * vector[1]
    new_y = sin_term * vector[0] + cos_term * vector[1]
    vector[0] = new_x
    vector[1] = new_y


def rotate_left(vector, angle):
    cos_term = cosinus(angle)
    sin_term = sinus(angle)
    rotate(vector, cos_term, sin_term)


def move(position, direction, instruction_value):
    move_east = direction[0] * instruction_value
    move_north = direction[1] * instruction_value
    position[0] += move_east
    position[1] += move_north


class Ship:
    def __init__(self):
        self.heading = [1, 0]
        self.position = [0, 0]
        self.waypoint = [10, 1]

        self.instructions = {
            'F': lambda v: move(self.position, self.heading, v),
            'N': lambda v: move(self.position, (0, 1), v),
            'S': lambda v: move(self.position, (0, -1), v),
            'E': lambda v: move(self.position, (1, 0), v),
            'W': lambda v: move(self.position, (-1, 0), v),
            'L': lambda v: rotate_left(self.heading, v),
            'R': lambda v: rotate_left(self.heading, 360 - v)
        }

        self.instructions_waypoint = {
            'F': lambda v: move(self.position, self.waypoint, v),
            'N': lambda v: move(self.waypoint, (0, 1), v),
            'S': lambda v: move(self.waypoint, (0, -1), v),
            'E': lambda v: move(self.waypoint, (1, 0), v),
            'W': lambda v: move(self.waypoint, (-1, 0), v),
            'L': lambda v: rotate_left(self.waypoint, v),
            'R': lambda v: rotate_left(self.waypoint, 360 - v)
        }

    @staticmethod
    def execute_instruction(instruction_code, instruction_value, instruction_set):
        instruction_callback = instruction_set[instruction_code]
        instruction_callback(instruction_value)

    def get_distance(self, distance=norm0):
        return distance(*self.position)


def parse_instruction(instruction: str):
    return instruction[0], int(instruction[1:])


def execute_all_instructions(filename, ship, instruction_set):
    with open(filename) as instructions:
        for instruction in instructions:
            instruction_code, instruction_value = parse_instruction(instruction)
            ship.execute_instruction(instruction_code, instruction_value, instruction_set)


def part1(filename):
    ship = Ship()
    instructions_set = ship.instructions
    execute_all_instructions(filename, ship, instructions_set)
    return ship.get_distance()


def part2(filename):
    ship = Ship()
    instructions_set = ship.instructions_waypoint
    execute_all_instructions(filename, ship, instructions_set)
    return ship.get_distance()


print(part1('d12'))
assert part1('d12') == 879
print(part2('d12'))
assert (part2('d12') == 18107)
