#!/usr/bin/env python3

import os
import sys


class Symbol:
    def __init__(self, x: int, y: int, value: str):
        self.x = x
        self.y = y
        self.value = value
        self.gear_ratio = 0

    def __repr__(self) -> str:
        coord = f"{self.x:<3} x {self.y:<3}"
        return f"{coord}: {self.value} {self.gear_ratio or ''}"


class Number:
    def __init__(self, x1: int, x2: int, y: int, value: int):
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.value = value
        self.is_partnumber = False

    def __repr__(self) -> str:
        coord = f"{self.x1:<3} ~ {self.x2:<3} x {self.y:<3}"
        return f"{coord}: {self.value}{'*' if self.is_partnumber else ''}"


def build_schematic(filename):
    numbers: list[Number] = []
    symbols: list[Symbol] = []
    with open(filename, "r", encoding="utf-8") as f:
        for y, line in enumerate(f.readlines()):
            current_number = []
            for x, c in enumerate(line):
                if c.isdigit():
                    current_number.append(c)
                    continue
                elif len(current_number) > 0:
                    value = int("".join(current_number))
                    numbers.append(
                        Number(
                            x1=x - len(current_number),
                            x2=x - 1,
                            y=y,
                            value=value,
                        )
                    )
                    current_number = []
                if c == "." or c == "\n":
                    continue
                symbols.append(
                    Symbol(
                        x=x,
                        y=y,
                        value=c,
                    )
                )
    for sym in symbols:
        adjacent_numbers = []
        for num in numbers:
            if num.y < sym.y - 1 or num.y > sym.y + 1:
                continue
            if num.x2 < sym.x - 1 or num.x1 > sym.x + 1:
                continue
            num.is_partnumber = True
            adjacent_numbers.append(num)
        if sym.value == "*" and len(adjacent_numbers) == 2:
            sym.gear_ratio = adjacent_numbers[0].value * adjacent_numbers[1].value
            print(sym)
    gear_ratios = [s.gear_ratio for s in symbols]
    print("Total:", sum(gear_ratios))


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    build_schematic(filename)
