#!/usr/bin/env python3

import os
import sys


def run(path: os.PathLike) -> str:
    with open(path, "r", encoding="ascii") as f:
        line = f.readline().strip()
    total = 0
    sequences = line.split(",")
    for sequence in sequences:
        value = 0
        for c in sequence:
            value += ord(c)
            value *= 17
            value %= 256
        total += value
        print(sequence, value)
    print("Total:", total)
    return str(total)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
