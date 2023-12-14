#!/usr/bin/env python3

import os
import sys


def run(path: os.PathLike) -> str:
    shape: list[str] = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                break
            shape.append(line)

    transposed = []
    for x in range(len(shape[0])):
        transposed_row = []
        for row in shape:
            transposed_row.append(row[x])
        transposed.append("".join(transposed_row))

    total_load = 0
    for column in transposed:
        shifted = []
        load = 0
        load_start = len(column)
        for space in column.split("#"):
            rocks = space.count("O")
            shifted.append(("O" * rocks).ljust(len(space), "."))
            # We use gaussian sum here
            load += int(rocks * (load_start * 2 - rocks + 1) / 2)
            load_start -= len(space) + 1
        total_load += load
        print("#".join(shifted), load)

    print("Total load:", total_load)
    return str(total_load)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
