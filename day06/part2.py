#!/usr/bin/env python3

import math
import os
import sys


CHARGE_RATE = 1.0


def read_numbers(line: str) -> list[float]:
    number_str = line.split(":", 1)[1].replace(" ", "")
    return int(number_str)


def minimum_distance(
    allocated_time: float, target_distance: float
) -> tuple[float, float]:
    """
    Let x = charge_time
        r = charge_rate
        t = allocated_time
        d = target_distance

    To win we need:
        (t - x) * x * r > d
        trx - rx^2 > d
        rx^2 - trx + d < 0

    Using roots of a binomial we can find the range of x required using:
            -b ± sqrt(b^2 - 4ac)
        x = --------------------
                    2a
    With:
        a = r
        b = -tr
        c = d
    """
    a = CHARGE_RATE
    b = allocated_time * CHARGE_RATE
    c = target_distance

    x1 = (b - math.sqrt(b**2 - 4.0 * a * c)) / (2.0 * a)
    x2 = (b + math.sqrt(b**2 - 4.0 * a * c)) / (2.0 * a)

    return (x1, x2)


def run(path: os.PathLike) -> str:
    with open(path, "r", encoding="utf-8") as f:
        time = read_numbers(f.readline().strip())
        distance = read_numbers(f.readline().strip())
        # We add 0.1mm to the distance to take into account the discrete
        # nature of how time and distances are calculated here.
        x1, x2 = minimum_distance(float(time), float(distance) + 0.1)
        x1 = math.ceil(x1)
        x2 = math.floor(x2)
        margin = x2 - x1 + 1
        print(f"Race: ({distance}mm@{time}ms) {x1}ms~{x2}ms (Margin: {margin})")
    print("Number of ways:", margin)
    return str(margin)


if __name__ == "__main__":
    filename = os.path.join(os.path.dirname(__file__), "input.txt")
    if len(sys.argv) > 1:
        filename = sys.argv[-1]
    run(filename)
