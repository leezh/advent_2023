#!/usr/bin/env python3

import os
import sys


def compare_lists(top: list[str], bottom: list[str], *, smudged: bool = False):
    has_smudge = False
    for a, b in zip(top, bottom):
        for x, y in zip(a, b):
            if x == y:
                continue
            if not smudged:
                return False
            if has_smudge:
                return False
            has_smudge = True
    if smudged and not has_smudge:
        return False
    return True


def find_mirror(shape: list[list[str]]) -> int:
    height = len(shape)
    width = len(shape[0])

    middle = height // 2 + 1
    for i in range(1, middle):
        top = shape[:i]
        bottom = [*reversed(shape[i : i + i])]
        if compare_lists(top, bottom, smudged=True):
            return i * 100
        j = height - i
        top = shape[j:]
        bottom = [*reversed(shape[j - i : j])]
        if compare_lists(top, bottom, smudged=True):
            return j * 100

    transposed = []
    for x in range(width):
        transposed_row = []
        for row in shape:
            transposed_row.append(row[x])
        transposed.append("".join(transposed_row))

    middle = width // 2 + 1
    for i in range(1, middle):
        top = transposed[:i]
        bottom = [*reversed(transposed[i : i + i])]
        if compare_lists(top, bottom, smudged=True):
            return i
        j = width - i
        top = transposed[j:]
        bottom = [*reversed(transposed[j - i : j])]
        if compare_lists(top, bottom, smudged=True):
            return j

    raise RuntimeError("No mirror found")


def run(path: os.PathLike) -> str:
    shapes: list[list[str]] = [[]]
    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                shapes.append([])
                continue
            shapes[-1].append(line)
    result = 0
    shapes = filter(None, shapes)
    for shape in shapes:
        print("\n".join(shape))
        if not shape:
            continue
        mirror = find_mirror(shape)
        print("Mirror point:", mirror)
        result += mirror
    print("Total:", result)
    return str(result)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
