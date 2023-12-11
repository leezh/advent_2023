#!/usr/bin/env python3

import os
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Self


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

    @property
    def inverse(self):
        if self == Direction.NORTH:
            return Direction.SOUTH
        if self == Direction.SOUTH:
            return Direction.NORTH
        if self == Direction.EAST:
            return Direction.WEST
        if self == Direction.WEST:
            return Direction.EAST
        raise KeyError


PIPE_EXITS: dict[str, tuple[Direction, Direction]] = {
    "|": (Direction.NORTH, Direction.SOUTH),
    "-": (Direction.EAST, Direction.WEST),
    "L": (Direction.NORTH, Direction.EAST),
    "J": (Direction.NORTH, Direction.WEST),
    "7": (Direction.SOUTH, Direction.WEST),
    "F": (Direction.SOUTH, Direction.EAST),
}


@dataclass
class Position:
    x: int
    y: int

    def moved(self, direction: Direction) -> Self:
        if direction == Direction.NORTH:
            return Position(self.x, self.y - 1)
        if direction == Direction.SOUTH:
            return Position(self.x, self.y + 1)
        if direction == Direction.EAST:
            return Position(self.x + 1, self.y)
        if direction == Direction.WEST:
            return Position(self.x - 1, self.y)
        raise KeyError

    def __hash__(self) -> int:
        return hash((self.x, self.y))


@dataclass
class Pipe:
    position: Position
    shape: str
    is_loop: bool = False

    def can_enter(self, entrance: Direction) -> bool:
        return entrance in PIPE_EXITS[self.shape]

    def follow(self, entrance: Direction) -> tuple[Direction, Position]:
        exits = PIPE_EXITS[self.shape]
        direction = exits[1] if entrance == exits[0] else exits[0]
        return direction, self.position.moved(direction)


class Maze:
    def __init__(self):
        self.width: int = 1
        self.height: int = 1
        self.pipes: dict[Position, Pipe] = {}
        self.start: Position | None = None

    def add_tile(self, position: Position, shape: str) -> None:
        if shape == "S":
            self.start = position
            return
        if shape not in PIPE_EXITS:
            return
        self.width = max(self.width, position.x)
        self.height = max(self.height, position.y)
        self.pipes[position] = Pipe(position, shape)

    def find_loop(self) -> None:
        for start_direction in Direction:
            direction = start_direction
            position = self.start.moved(direction)
            while position in self.pipes:
                pipe = self.pipes[position]
                if not pipe.can_enter(direction.inverse):
                    break
                if pipe.is_loop:
                    break
                pipe.is_loop = True
                direction, position = pipe.follow(direction.inverse)
                if position == self.start:
                    for position, pipe in [*self.pipes.items()]:
                        if pipe.is_loop:
                            continue
                        del self.pipes[position]
                    for shape, exits in PIPE_EXITS.items():
                        if direction.inverse in exits and start_direction in exits:
                            self.pipes[self.start] = Pipe(self.start, shape, True)
                            break
                    return
            for pipe in self.pipes.values():
                pipe.is_loop = False
        raise RuntimeError("Could not find loop")

    def is_inside(self, position: Position) -> bool:
        vertical = 0
        for x in range(1, position.x):
            sample = Position(x, position.y)
            if sample not in self.pipes:
                continue
            exits = PIPE_EXITS[self.pipes[sample].shape]
            if Direction.NORTH in exits:
                vertical += 1
        if (vertical % 2) == 1:
            return True

        horizontal = 0
        for y in range(1, position.y):
            sample = Position(position.x, y)
            if sample not in self.pipes:
                continue
            exits = PIPE_EXITS[self.pipes[sample].shape]
            if Direction.EAST in exits:
                horizontal += 1
        return (horizontal % 2) == 1


def run(path: os.PathLike) -> str:
    maze = Maze()

    with open(path, "r", encoding="utf-8") as f:
        for y, line in enumerate(f.readlines(), 1):
            line = line.strip()
            if not line:
                break
            for x, c in enumerate(line, 1):
                maze.add_tile(Position(x, y), c)

    maze.find_loop()

    result = 0

    for y in range(1, maze.height + 1):
        line: list[str] = []
        for x in range(1, maze.width + 1):
            position = Position(x, y)
            if position in maze.pipes:
                line.append(maze.pipes[position].shape)
            elif maze.is_inside(position):
                result += 1
                line.append("#")
            else:
                line.append(" ")
        print("".join(line))

    print("Total Enclosed Tiles:", result)
    return str(result)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
