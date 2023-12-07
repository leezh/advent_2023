#!/usr/bin/env python3

import os
import sys
from dataclasses import dataclass
from typing import Self

CARD_STRENGTH = "J23456789TQKA"
HAND_TYPES = [
    "High Card",
    "One Pair",
    "Two Pair",
    "Three of a Kind",
    "Full House",
    "Four of a Kind",
    "Five of a Kind",
]


def hand_strength(hand: str):
    jokers = hand.count("J")
    hand = hand.replace("J", "")
    card_count: dict[str, int] = {}
    for card in hand:
        if card in card_count:
            card_count[card] += 1
        else:
            card_count[card] = 1
    number_of_cards = sorted(card_count.values(), reverse=True)
    if jokers == 5 or number_of_cards[0] + jokers == 5:
        return 6
    if jokers == 4 or number_of_cards[0] + jokers == 4:
        return 5
    if jokers == 3:
        if number_of_cards[0] == 2:
            return 4
        return 3
    if number_of_cards[0] + jokers == 3:
        if number_of_cards[1] == 2:
            return 4
        return 3
    if jokers == 2:
        if number_of_cards[0] == 2:
            return 2
        return 1
    if number_of_cards[0] + jokers == 2:
        if number_of_cards[1] == 2:
            return 2
        return 1
    return 0


@dataclass
class Player:
    hand: str
    bid: int
    strength: int
    card_strengths: list[int]
    rank: int = 0
    winnings: int = 0

    def __repr__(self) -> str:
        return f"Hand: {self.hand} ({HAND_TYPES[self.strength]} [{self.rank}]) @ ${self.bid} and Wins ${self.winnings}"

    def __lt__(self, cmp: Self):
        if self.strength != cmp.strength:
            return self.strength < cmp.strength
        return self.card_strengths < cmp.card_strengths


def run(path: os.PathLike) -> str:
    with open(path, "r", encoding="utf-8") as f:
        players: list[Player] = []
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            hand, bid = line.split(" ", 1)
            players.append(
                Player(
                    hand,
                    int(bid),
                    hand_strength(hand),
                    [CARD_STRENGTH.index(c) for c in hand],
                )
            )
    result = 0
    for rank, player in enumerate(sorted(players), 1):
        player.rank = rank
        player.winnings = rank * player.bid
        result += player.winnings
    for player in players:
        print(player)
    print("Total Winnings:", result)
    return str(result)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
