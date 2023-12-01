#!/usr/bin/env python3

import os
import re
import sys


STR_NUMBERS = [
    "[0-9]",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]

filename = os.path.join(os.path.dirname(__file__), "input.txt")
if len(sys.argv) > 1:
    filename = sys.argv[-1]


def convert_number(text):
    if text not in STR_NUMBERS:
        return int(text)
    return STR_NUMBERS.index(text)


with open(filename, "r", encoding="utf-8") as f:
    numbers: list[int] = []
    pattern = re.compile(f"(?=({'|'.join(STR_NUMBERS)}))")
    for line in f.readlines():
        first_digit: int | None = None
        for match in pattern.finditer(line):
            if first_digit is None:
                first_digit = convert_number(match.group(1))
            last_digit = convert_number(match.group(1))
        if first_digit is None:
            print(line.strip())
            continue
        number = first_digit * 10 + last_digit
        print(number, "<-", line.strip())
        numbers.append(number)
    print("Total:", sum(numbers))
