from typing import Set, Dict


class Letter:
    predecessors: Set[str]
    successors: Set[str]

    def __init__(self, letter: str):
        self.letter = letter
        self.predecessors = {letter}
        self.successors = {letter}


def add_successors(parent_letter: str, child_letter: str, letter_graph: Dict[str, 'Letter']):
    parent_letter_instance = get_or_create_letter(parent_letter, letter_graph)
    if child_letter in parent_letter_instance.successors:
        return
    child_letter_instance = get_or_create_letter(child_letter, letter_graph)
    child_letter_instance.predecessors.update(parent_letter_instance.predecessors)
    for great_parent_letter in parent_letter_instance.predecessors:
        letter_graph[great_parent_letter].successors.add(child_letter)


def get_or_create_letter(letter: str, letter_graph: Dict[str, Letter]):
    if letter not in letter_graph:
        letter_graph[letter] = Letter(letter)
    return letter_graph[letter]


def get_order(letter_graph: Dict[str, Letter]):
    sorted_letters = sorted(letter_graph.values(), key=lambda letter: len(letter.successors),
                            reverse=True)
    return [l.letter for l in sorted_letters]


def add_word_to_graph(word, letter_graph):
    for index_parent_letter, parent_letter in enumerate(word):
        for child_letter in word[index_parent_letter:]:
            add_successors(parent_letter, child_letter, letter_graph)


def get_ordered_letters(filename):
    letter_graph = dict()
    with open(filename) as words:
        for word in words:
            add_word_to_graph(word.strip(), letter_graph)
    return get_order(letter_graph)


print(get_ordered_letters('alphaorder'))
