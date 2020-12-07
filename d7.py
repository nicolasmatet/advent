import string
from typing import Dict, Tuple, List, Set
import re

from utils.files import read_file

regex_container = '(.+) bags'
regex_content = '(([0-9]+) ([^,.]+)) bag[s]?'


class Node:

    def __init__(self, label):
        self.label = label
        self.contains = dict()
        self.is_contained = set()
        self.number_contained = None

    def add_content(self, name, mult):
        self.contains[name] = mult

    def add_container(self, name):
        self.is_contained.add(name)

    def containers(self):
        return self.is_contained

    def containeds(self):
        return self.contains


class Digraph:
    nodes: Dict

    def __init__(self):
        self.nodes = dict()

    def get_node(self, name) -> Node:
        return self.nodes.get(name)

    def get_or_create_node(self, name):
        if name not in self.nodes:
            new_node = Node(name)
            self.nodes[name] = new_node
        return self.nodes[name]

    def add_node(self, container, content):
        new_node = self.get_or_create_node(container)
        self.nodes[container] = new_node
        self.add_node_content(new_node, content)

    def add_node_content(self, node, content):
        for contained, mult in content:
            contained_node = self.get_or_create_node(contained)
            node.add_content(contained, mult)
            contained_node.add_container(node.label)


def build_digraph(filename):
    digraph = Digraph()
    with read_file(filename) as rules:
        for rule in rules:
            container, content = parse_rule(rule)
            digraph.add_node(container, content)
    return digraph


def parse_rule(rule: str):
    splitted = rule.split('contain')
    container = get_container(splitted[0])
    content = get_content(splitted[1])
    return container, content


def get_container(rule_part: string):
    return re.match(regex_container, rule_part).groups()[0]


def get_content(rule_part: str):
    all_content = re.findall(regex_content, rule_part)
    return [(contained, int(mult)) for _, mult, contained in all_content]


def get_number_of_containers(contained: str, set_visited: Set[str], digraph: Digraph):
    cur_node = digraph.get_node(contained)
    number_of_containers = 0
    for container in cur_node.containers():
        if container in set_visited:
            continue
        number_of_containers += 1
        set_visited.add(container)
        additional_containers = get_number_of_containers(container, set_visited, digraph)
        number_of_containers += additional_containers
    return number_of_containers


def get_number_of_contained(container: str, digraph: Digraph):
    cur_node = digraph.get_node(container)
    if cur_node.number_contained is not None:
        return cur_node.number_contained

    number_of_contained = 0
    for contained, mult in cur_node.containeds().items():
        additionnal_contained = get_number_of_contained(contained, digraph)
        number_of_contained += mult * (1 + additionnal_contained)
    cur_node.number_contained = number_of_contained
    return number_of_contained


def part1():
    digraph = build_digraph('d7')
    return get_number_of_containers('shiny gold', set(), digraph)


def part2():
    digraph = build_digraph('d7')
    return get_number_of_contained('shiny gold', digraph)


print(part1())
print(part2())

assert part1() == 213
assert part2() == 38426
