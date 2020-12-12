import networkx as nx


def get_outputs(filename):
    with open(filename) as f:
        return [int(r) for r in f.readlines()]


def get_sorted_voltages(filename):
    output_voltages = get_outputs(filename)
    last_voltage = max(output_voltages) + 3
    output_voltages.extend([0, last_voltage])
    output_voltages.sort()
    return output_voltages


def get_digraph_edges(output_voltages):
    other_edges = []
    for idx in range(0, len(output_voltages) - 1):
        other_edges.extend(get_node_successors(idx, output_voltages))
    return other_edges


def get_node_successors(idx, output_voltages):
    successors = []
    next_idx = idx + 1
    while (v := output_voltages[next_idx]) - (u := output_voltages[idx]) < 4:
        successors.append((u, v))
        next_idx += 1
        if next_idx == len(output_voltages):
            break
    return successors


def count_path(origin, dest, digraph: nx.DiGraph):
    if origin == dest:
        return 1
    if digraph.nodes[origin]["count_paths"] is not None:
        return digraph.nodes[origin]["count_paths"]
    count_paths = 0
    for neighbor in digraph.successors(origin):
        count_paths += count_path(neighbor, dest, digraph)
    nx.set_node_attributes(digraph, {origin: count_paths}, "count_paths")
    return count_paths


def part1():
    output_voltages = get_sorted_voltages('d10')
    differences = [next_v - previous_v for next_v, previous_v in zip(output_voltages[1:], output_voltages[0:-1])]
    count3 = differences.count(3)
    count1 = differences.count(1)
    return count1 * count3


def part2():
    output_voltages = get_sorted_voltages('d10')
    g = nx.DiGraph()
    g.add_nodes_from(output_voltages)
    g.add_edges_from(get_digraph_edges(output_voltages))
    nx.set_node_attributes(g, None, "count_paths")
    return count_path(0, output_voltages[-1], g)


print(part1())
print(part2())

assert part1() == 2368
assert part2() == 1727094849536


def part3():
    output_voltages = get_sorted_voltages('d10')
    g = nx.DiGraph()
    g.add_nodes_from(output_voltages)
    g.add_edges_from(get_digraph_edges(output_voltages))
    nx.set_node_attributes(g, None, "count_paths")

    def dist(n1, n2):
        return 1

    return nx.astar_path(g, output_voltages[0], output_voltages[-1], dist)


print(len(part3()))
