#!/usr/bin/env python3

import os
import sys
from dataclasses import dataclass


EXPANSION = 1000000


@dataclass
class Position:
    x: int
    y: int


def run(path: os.PathLike) -> str:
    width = 0
    height = 0
    galaxies: list[Position] = []
    occupied_rows: list[int] = []
    occupied_columns: list[int] = []

    with open(path, "r", encoding="utf-8") as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            if not line:
                break
            height += 1
            width = len(line)
            for x, c in enumerate(line):
                if c != "#":
                    continue
                if x not in occupied_columns:
                    occupied_columns.append(x)
                if y not in occupied_rows:
                    occupied_rows.append(y)
                galaxies.append(Position(x, y))

    empty_columns = [x for x in range(width) if x not in occupied_columns]
    empty_rows = [x for x in range(height) if x not in occupied_rows]

    for i, x in enumerate(empty_columns):
        for galaxy in galaxies:
            if galaxy.x < x + i * (EXPANSION - 1):
                continue
            galaxy.x += EXPANSION - 1

    for i, y in enumerate(empty_rows):
        for galaxy in galaxies:
            if galaxy.y < y + i * (EXPANSION - 1):
                continue
            galaxy.y += EXPANSION - 1

    distances: list[int] = []
    for i, a in enumerate(galaxies):
        for j, b in enumerate(galaxies[i + 1 :], i + 1):
            distance = abs(a.x - b.x) + abs(a.y - b.y)
            distances.append(distance)
            print(f"{i + 1} & {j + 1}: {distance}")

    result = sum(distances)
    print("Total Distances:", result)
    return str(result)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
