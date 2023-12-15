#!/usr/bin/env python3

import os
import re
import sys
from collections import OrderedDict

label_pattern = re.compile("([a-zA-Z]+)(-|=([1-9]))")


def run(path: os.PathLike) -> str:
    with open(path, "r", encoding="ascii") as f:
        line = f.readline().strip()

    boxes: dict[int, OrderedDict[str, int]] = {}

    sequences = line.split(",")
    for sequence in sequences:
        matches = label_pattern.match(sequence)
        label = matches.group(1)
        focal_length = matches.group(3)
        box_id = 0
        for c in label:
            box_id += ord(c)
            box_id *= 17
            box_id %= 256
        if focal_length is not None:
            if box_id not in boxes:
                boxes[box_id] = OrderedDict()
            boxes[box_id][label] = int(focal_length)
        elif box_id in boxes and label in boxes[box_id]:
            del boxes[box_id][label]

    total = 0
    for box_id, lenses in boxes.items():
        for slot, focal_length in enumerate(lenses.values(), 1):
            power = (box_id + 1) * slot * focal_length
            total += power
    print("Total:", total)
    return str(total)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
