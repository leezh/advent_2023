#!/usr/bin/env python3

import os
import re
import sys
from dataclasses import dataclass, field

required_seeds_pattern = re.compile(r"seeds: ([0-9 ]+)")
map_header_pattern = re.compile(r"(\w+)-to-(\w+) map:")
map_range_pattern = re.compile(r"([0-9+])\s+([0-9]+)\s+([0-9]+)")


@dataclass
class Range:
    start: int = 0
    end: int = 0

    def __repr__(self) -> str:
        return f"{self.start}~{self.end}"


@dataclass
class MapperRange:
    start: int = 0
    end: int = 0
    offset: int = 0

    def __repr__(self) -> str:
        return f"{self.start}~{self.end} ({self.offset:+})"

    def intersect(self, values: Range) -> list[Range] | None:
        if values.start < self.start:
            if values.end < self.start:
                return None
            if values.end <= self.end:
                return [
                    Range(self.start + self.offset, values.end + self.offset),
                    Range(values.start, self.start - 1),
                ]
            return [
                Range(self.start + self.offset, self.end + self.offset),
                Range(values.start, self.start - 1),
                Range(self.end + 1, values.end),
            ]
        if values.start <= self.end:
            if values.end <= self.end:
                return [
                    Range(values.start + self.offset, values.end + self.offset),
                ]
            return [
                Range(values.start + self.offset, self.end + self.offset),
                Range(self.end + 1, values.end),
            ]
        return None


@dataclass
class Mapper:
    src: str
    dest: str
    sections: list[MapperRange] = field(default_factory=list)

    def add_section(self, section: MapperRange) -> None:
        self.sections.append(section)

    def map_value(self, values: list[Range]) -> list[Range]:
        queue = [*values]
        results = []
        while len(queue) > 0:
            subrange = queue.pop(0)
            is_mapped = False
            for section in self.sections:
                cuts = section.intersect(subrange)
                if cuts is not None:
                    is_mapped = True
                    results.append(cuts[0])
                    if len(cuts) > 1:
                        queue.extend(cuts[1:])
                    break
            if not is_mapped:
                results.append(subrange)
        return results

    def __repr__(self) -> str:
        return f"{self.src}-to-{self.dest}"


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
                seed_array = [int(x) for x in search.group(1).split(" ") if x]
                required_seeds = []
                for i in range(0, len(seed_array), 2):
                    start = seed_array[i]
                    end = start + seed_array[i + 1] - 1
                    required_seeds.append(
                        Range(
                            start=start,
                            end=end,
                        )
                    )
            elif current_map is None:
                search = map_header_pattern.match(line)
                current_map = Mapper(
                    src=search.group(1),
                    dest=search.group(2),
                )
                maps[current_map.src] = current_map
            else:
                values = [int(x) for x in line.split(" ") if x]
                start = values[1]
                end = start + values[2] - 1
                offset = values[0] - start
                section = MapperRange(
                    start=start,
                    end=end,
                    offset=offset,
                )
                current_map.add_section(section)

    chain: list[Mapper] = [maps["seed"]]
    while chain[-1].dest in maps:
        chain.append(maps[chain[-1].dest])

    required_locations = []
    for seeds in required_seeds:
        print("=" * 20)
        print(seeds)
        locations = [seeds]
        for mapper in chain:
            locations = mapper.map_value(locations)
        required_locations.extend(locations)
        print(locations)

    result = min(l.start for l in required_locations)
    print("Closest locaiton:", result)
    return str(result)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
