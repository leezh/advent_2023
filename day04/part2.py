#!/usr/bin/env python3

import os
import re
import sys


card_regex = re.compile(r"Card\s+([0-9]+): ([0-9 ]+)\|([0-9 ]+)")


class Card:
    def __init__(self, card_id: int, winning_numbers: list[int], owned_numbers: list[int]) -> None:
        self.card_id = card_id
        self.winning_numbers = winning_numbers
        self.owned_numbers = owned_numbers
        self.score = 0
        self.instances = 1

    def __repr__(self) -> str:
        return f"Card {self.card_id} Score: {self.score} x {self.instances}"


def run(path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        cards: list[Card] = []
        for line in f.readlines():
            matches = card_regex.match(line)
            if matches is None:
                continue
            card_id = int(matches.group(1))
            winning_numbers = [int(x) for x in matches.group(2).split(" ") if x]
            owned_numbers = [int(x) for x in matches.group(3).split(" ") if x]
            cards.append(Card(card_id, winning_numbers, owned_numbers,))
        for i, c in enumerate(cards):
            instances = c.instances
            for number in c.owned_numbers:
                if number in c.winning_numbers:
                    c.score += 1
            for offset in range(1, c.score + 1):
                cards[i + offset].instances += instances
            print(c)
        card_instances = [c.instances for c in cards]
        result = sum(card_instances)
        print("Total:", result)
    return str(result)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
