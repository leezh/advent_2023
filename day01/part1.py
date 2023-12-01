#!/usr/bin/env python3

import os
import sys

filename = os.path.join(os.path.dirname(__file__), 'input.txt')
if len(sys.argv) > 1:
    filename = sys.argv[-1]

with open(filename, "r", encoding="utf-8") as f:
    numbers: list[int] = []
    for line in f.readlines():
        first_digit: int | None = None
        for c in line:
            if c.isnumeric():
                if first_digit is None:
                    first_digit = int(c)
                last_digit = int(c)
        if first_digit is None:
            print(line.strip())
            continue
        number = first_digit * 10 + last_digit
        print(number, '<-', line.strip())
        numbers.append(number)
    print('Total:', sum(numbers))

