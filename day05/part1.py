#!/usr/bin/env python3

import os
import re
import sys
from dataclasses import dataclass, field

required_seeds_pattern = re.compile(r"seeds: ([0-9 ]+)")
map_header_pattern = re.compile(r"(\w+)-to-(\w+) map:")
map_range_pattern = re.compile(r"([0-9+])\s+([0-9]+)\s+([0-9]+)")


@dataclass
class MapperRange:
    dest: int = 0
    src: int = 0
    size: int = 0

    def __contains__(self, value: int) -> bool:
        return value >= self.src and value <= self.src + self.size

    def __getitem__(self, index: int) -> int:
        return index - self.src + self.dest


@dataclass
class Mapper:
    src: str
    dest: str
    sections: list[MapperRange] = field(default_factory=list)

    def add_section(self, section: MapperRange) -> None:
        self.sections.append(section)

    def __getitem__(self, index: int) -> int:
        for r in self.sections:
            if index in r:
                return r[index]
        return index


def run(path) -> str:
    required_seeds: list[int] | None = None
    current_map: Mapper | None = None
    maps: dict[str, Mapper] = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                current_map = None
            elif required_seeds is None:
                search = required_seeds_pattern.match(line)
                required_seeds = [int(x) for x in search.group(1).split(" ") if x]
            elif current_map is None:
                search = map_header_pattern.match(line)
                current_map = Mapper(
                    src=search.group(1),
                    dest=search.group(2),
                )
                maps[current_map.src] = current_map
            else:
                values = [int(x) for x in line.split(" ") if x]
                section = MapperRange(
                    dest=values[0],
                    src=values[1],
                    size=values[2],
                )
                current_map.add_section(section)

    chain: list[Mapper] = [maps["seed"]]
    while chain[-1].dest in maps:
        chain.append(maps[chain[-1].dest])
    print("Conversion chain:", " -> ".join(["seed", *[c.dest for c in chain]]))

    required_locations = []
    for seed in required_seeds:
        location = seed
        for mapper in chain:
            location = mapper[location]
        required_locations.append(location)
        print("Seed:", seed, "-> Location:", location)

    result = min(required_locations)
    print("Closest locaiton:", result)
    return str(result)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
