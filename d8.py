from typing import Set


def get_instructions(filename):
    with open(filename) as f:
        instructions = f.readlines()
        return [build_instruction(line) for line in instructions]


def build_instruction(line):
    splitted = line.strip().split(' ')
    return splitted[0], int(splitted[1])


class State:
    acc_value: int
    index: int
    set_executed: Set[int]

    def __init__(self, instructions):
        self.all_instructions = instructions
        self.reset()
        self.reset()

    def reset(self):
        self.acc_value = 0
        self.index = 0
        self.set_executed = set()

    def execute_to_termination(self):
        while self.execute_step():
            continue
        return self.has_terminate()

    def execute_step(self):
        if self.in_loop() or self.has_terminate():
            return False
        self.set_executed.add(self.index)
        instruction_code, instruction_value = self.all_instructions[self.index]
        self.run_instruction(instruction_code, instruction_value)
        return True

    def in_loop(self):
        return self.index in self.set_executed

    def has_terminate(self):
        return self.index == len(self.all_instructions)

    def run_instruction(self, instruction_code, instruction_value):
        getattr(self, instruction_code)(instruction_value)

    def nop(self, value):
        self.index += 1

    def acc(self, value):
        self.acc_value += value
        self.index += 1

    def jmp(self, value):
        self.index += value

    def switch(self, index_to_switch):
        return self.switch_instuctions(self.all_instructions, index_to_switch)

    def switch_back(self, switched_index):
        if switched_index is not None:
            self.switch_instuctions(self.all_instructions, switched_index)

    @staticmethod
    def switch_instuctions(all_instructions, switched_index):
        instruction_code, instruction_value = all_instructions[switched_index]
        if instruction_code == 'jmp':
            all_instructions[switched_index] = ('nop', instruction_value)
            return switched_index
        if instruction_code == 'nop':
            all_instructions[switched_index] = ('jmp', instruction_value)
            return switched_index
        return None


def part1():
    all_instructions = get_instructions('d8')
    state = State(all_instructions)
    state.execute_to_termination()
    return state.acc_value


def part2():
    all_instructions = get_instructions('d8')
    switched_index = None
    index_to_switch = 0
    state = State(all_instructions)
    while not state.has_terminate():
        switched_index = execute_with_index_switch(state, index_to_switch, switched_index)
        index_to_switch += 1
    return state.acc_value


def execute_with_index_switch(state, index_to_switch, switched_index):
    state.switch_back(switched_index)
    switched_index = state.switch(index_to_switch)
    state.reset()
    if switched_index:
        state.execute_to_termination()
    return switched_index


print('part1', part1())
print('part2', part2())

assert part1() == 1584
assert part2() == 920
