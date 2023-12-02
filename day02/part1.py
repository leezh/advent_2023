#!/usr/bin/env python3

import re
import os
import sys

filename = os.path.join(os.path.dirname(__file__), "input.txt")
if len(sys.argv) > 1:
    filename = sys.argv[-1]

max_colours = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

game_pattern = re.compile(r"Game ([0-9]+)")
hand_pattern = re.compile(r"([0-9]+) (blue|red|green)")

with open(filename, "r", encoding="utf-8") as f:
    possible_games: list[int] = []
    for line in f.readlines():
        game_str, data_str = line.split(":", 1)
        game_id = int(game_pattern.match(game_str).group(1))
        impossible_hand = False
        for hand_str in data_str.split(";"):
            for cubes in hand_pattern.finditer(hand_str):
                number = int(cubes.group(1))
                colour = cubes.group(2)
                if max_colours[colour] < number:
                    impossible_hand = True
        print("Game", game_id, "Impossible" if impossible_hand else "OK")
        if impossible_hand:
            continue
        possible_games.append(game_id)
    print("Sum of Possible Game IDs:", sum(possible_games))
