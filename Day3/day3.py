#!/bin/env python

import re


def get_product(pair: str) -> int:
    tmp = pair.split(",")
    return int(tmp[0][4:]) * int(tmp[1][:-1])


def main() -> None:
    multiply_pairs: list[str] = []

    with open("input.txt") as f:
        for line in f.readlines():
            multiply_pairs.extend(re.findall(r"mul\(\d+,\d+\)", line))

    print(f"Part 1: {sum([get_product(pair) for pair in multiply_pairs])}")

    instructions: list[list[str]] = []

    with open("input.txt") as f:
        for line in f.readlines():
            instructions.extend(
                re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", line)
            )

    total_sum = 0
    do = True
    for inst in instructions:
        if inst == "do()":
            do = True
            continue

        if inst == "don't()":
            do = False
            continue

        if do:
            total_sum += get_product(inst)

    print(f"Part 2: {total_sum}")


if __name__ == "__main__":
    main()
