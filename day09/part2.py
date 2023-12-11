#!/usr/bin/env python3

import os
import sys
from itertools import pairwise


def predict(sequence: list[int]) -> int:
    difference = [y - x for (x, y) in pairwise(sequence)]
    if all(x == 0 for x in difference):
        return sequence[0]
    prediction = sequence[0] - predict(difference)
    return prediction


def run(path: os.PathLike) -> str:
    totals: list[int] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            sequence = [int(x) for x in line.split(" ")]
            prediction = predict(sequence)
            print(prediction, sequence)
            totals.append(prediction)
    result = sum(totals)
    print("Sum of predictions:", result)
    return str(result)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
