#!/usr/bin/env python3

import itertools
import os
import sys


def is_possible_layout(records: str, groupings: list[int], offsets: list[int]) -> bool:
    for size, offset, next_offset in zip(groupings[:-1], offsets[:-1], offsets[1:]):
        if size + offset >= next_offset:
            return False
    for position, c in enumerate(records):
        if c == "?":
            continue
        is_group = False
        for size, offset in zip(groupings, offsets):
            if offset <= position < offset + size:
                is_group = True
                break
        if (c == "#") != is_group:
            return False
    return True


def run(path: os.PathLike) -> str:
    total_arrangements = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            records, groupings = line.split(" ", 1)
            groupings = [int(x) for x in groupings.split(",")]

            group_positions: list[list[int]] = []
            for i, size in enumerate(groupings):
                positions: list[int] = []
                start = sum(groupings[:i]) + i
                end = len(records) - sum(groupings[i:]) - len(groupings) + i + 1
                for offset in range(start, end + 1):
                    if offset > 0 and records[offset - 1] == "#":
                        continue
                    if offset + size < len(records) and records[offset + size] == "#":
                        continue
                    if "." in records[offset:offset+ size]:
                        continue
                    positions.append(offset)
                group_positions.append(positions)

            record_arrangements = 0
            for offsets in itertools.product(*group_positions):
                if is_possible_layout(records, groupings, offsets):
                    record_arrangements += 1
            total_arrangements += record_arrangements
            print(records, groupings, "->", record_arrangements)

    print("Total arrangements:", total_arrangements)
    return str(total_arrangements)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
