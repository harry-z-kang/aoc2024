#!/bin/env python


from collections import defaultdict
from copy import deepcopy


def get_stone_count(numbers: list[int], iterations: int) -> int:
    num_count = defaultdict(int)
    for num in numbers:
        num_count[num] += 1

    for _ in range(iterations):
        next_cycle_num_count = deepcopy(num_count)
        for number, count in num_count.items():
            next_cycle_num_count[number] -= count

            if number == 0:
                next_cycle_num_count[1] += count
                continue

            num_str = str(number)
            if len(num_str) % 2 == 0:
                left = num_str[: len(num_str) // 2]
                right = num_str[len(num_str) // 2 :]
                next_cycle_num_count[int(left)] += count
                next_cycle_num_count[int(right)] += count
                continue

            next_cycle_num_count[number * 2024] += count
        num_count = next_cycle_num_count

    return sum(list(num_count.values()))


def main() -> None:
    with open("input.txt") as f:
        numbers = [int(x) for x in f.read().strip().split()]

        print(f"Part 1: {get_stone_count(numbers, 25)}")
        print(f"Part 2: {get_stone_count(numbers, 75)}")


if __name__ == "__main__":
    main()
