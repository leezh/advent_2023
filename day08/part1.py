#!/usr/bin/env python3

import os
import re
import sys
from dataclasses import dataclass


node_pattern = re.compile(r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)")

@dataclass
class Node:
    name: str
    left_exit: str
    right_exit: str

    def __repr__(self) -> str:
        return f"<node {self.name}>"


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
    current_node = nodes["AAA"]
    while current_node.name != "ZZZ":
        for direction in instructions:
            if direction == "L":
                next_node = nodes[current_node.left_exit]
            elif direction == "R":
                next_node = nodes[current_node.right_exit]
            else:
                raise KeyError
            print(current_node, "->", direction, "->", next_node)
            current_node = next_node
            result += 1
            if current_node.name == "ZZZ":
                break
    print("Steps:", result)
    return str(result)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
