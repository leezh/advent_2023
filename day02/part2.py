#!/usr/bin/env python3

import re
import os
import sys

filename = os.path.join(os.path.dirname(__file__), "input.txt")
if len(sys.argv) > 1:
    filename = sys.argv[-1]

game_pattern = re.compile(r"Game ([0-9]+)")
hand_pattern = re.compile(r"([0-9]+) (blue|red|green)")

with open(filename, "r", encoding="utf-8") as f:
    powers: list[int] = []
    for line in f.readlines():
        game_str, data_str = line.split(":", 1)
        game_id = int(game_pattern.match(game_str).group(1))
        max_colours = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for hand_str in data_str.split(";"):
            for cubes in hand_pattern.finditer(hand_str):
                number = int(cubes.group(1))
                colour = cubes.group(2)
                max_colours[colour] = max(max_colours[colour], number)
        power = 1
        for number in max_colours.values():
            power *= number
        print("Game", game_id, "Power", power)
        powers.append(power)
    print("Sum of Game Power:", sum(powers))
