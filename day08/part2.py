#!/usr/bin/env python3

import math
import os
import re
import sys
from dataclasses import dataclass


node_pattern = re.compile(r"([0-9A-Z]+) = \(([0-9A-Z]+), ([0-9A-Z]+)\)")

@dataclass
class Node:
    name: str
    left_exit: str
    right_exit: str

    def __repr__(self) -> str:
        return f"Node {self.name} [{self.left_exit} | {self.right_exit}]"

    @property
    def is_start(self):
        return self.name.endswith("A")

    @property
    def is_end(self):
        return self.name.endswith("Z")


def run(path: os.PathLike) -> str:
    instructions: str | None = None
    nodes: dict[str, Node] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            if instructions is None:
                instructions = line
                continue
            matches = node_pattern.match(line)
            node = Node(
                matches.group(1),
                matches.group(2),
                matches.group(3),
            )
            nodes[node.name] = node
    result = 0

    instances = [n for n in nodes.values() if n.is_start]
    steps = [0] * len(instances)
    print(instances)
    while not all(n.is_end for n in instances):
        for direction in instructions:
            next_nodes = []
            for index, node in enumerate(instances):
                if node.is_end:
                    next_nodes.append(node)
                    continue
                if direction == "L":
                    next_nodes.append(nodes[node.left_exit])
                elif direction == "R":
                    next_nodes.append(nodes[node.right_exit])
                else:
                    raise KeyError
                steps[index] += 1
            print(direction, "->", next_nodes)
            instances = next_nodes
            if all(n.is_end for n in instances):
                break
    print("Steps:", steps)
    result = math.lcm(*steps)
    print("Total Steps:", result)
    return str(result)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
