#!/usr/bin/env python3

import os
import sys
from dataclasses import dataclass
from enum import Enum
from math import ceil
from typing import Callable, Self


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
    depth: int = 0

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

    def follow(self, direction: Direction) -> tuple[bool, int]:
        position = self.start.moved(direction)
        depth = 0
        while position in self.pipes:
            pipe = self.pipes[position]
            if not pipe.can_enter(direction.inverse):
                break
            if pipe.depth != 0:
                break
            depth += 1
            pipe.depth = depth
            direction, position = pipe.follow(direction.inverse)
            if position == self.start:
                return True, depth
        return False, depth

    def reset(self) -> None:
        for pipe in self.pipes.values():
            pipe.depth = 0

    def render(self, func: Callable[[Pipe], str], *, pad: int = 1) -> None:
        lines: list[str] = []
        for y in range(1, self.height + 1):
            line: list[str] = []
            for x in range(1, self.width + 1):
                position = Position(x, y)
                if position == self.start:
                    line.append("S".center(pad))
                elif position in self.pipes:
                    pipe = self.pipes[position]
                    line.append(func(pipe).center(pad))
                else:
                    line.append(".".center(pad))
            lines.append("".join(line))
        return "\n".join(lines)


def run(path: os.PathLike) -> str:
    maze = Maze()

    with open(path, "r", encoding="utf-8") as f:
        for y, line in enumerate(f.readlines(), 1):
            line = line.strip()
            if not line:
                break
            for x, c in enumerate(line, 1):
                maze.add_tile(Position(x, y), c)

    complete: bool = False
    depth: int = 0

    print("Shape:")
    print(maze.render(lambda x: x.shape))

    for direction in Direction:
        print(direction)
        complete, depth = maze.follow(direction)
        print(
            maze.render(lambda x: str(x.depth) if x.depth else ".", pad=len(str(depth)))
        )
        if complete:
            break
        maze.reset()

    if not complete:
        raise RuntimeError("Could not find loop")

    result = ceil(float(depth) / 2.0)
    print("Max Depth:", result)

    return str(result)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
