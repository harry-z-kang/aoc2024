#!/bin/env python


import math


def get_antinodes_part1(
    antenna_map: list[str], antenna1: tuple[int, int], antenna2: tuple[int, int]
) -> list[tuple[int, int]]:
    dx = antenna1[0] - antenna2[0]
    dy = antenna1[1] - antenna2[1]

    antinodes = [
        antinode
        for antinode in [
            (antenna1[0] + dx, antenna1[1] + dy),
            (antenna1[0] - dx, antenna1[1] - dy),
            (antenna2[0] + dx, antenna2[1] + dy),
            (antenna2[0] - dx, antenna2[1] - dy),
        ]
        if antinode not in [antenna1, antenna2]
        and 0 <= antinode[0] < len(antenna_map)
        and 0 <= antinode[1] < len(antenna_map[0])
    ]

    return antinodes


def get_antinodes_part2(
    antenna_map: list[str], antenna1: tuple[int, int], antenna2: tuple[int, int]
) -> list[tuple[int, int]]:
    dx = antenna1[0] - antenna2[0]
    dy = antenna1[1] - antenna2[1]

    antinodes = list[tuple[int, int]]()

    for antenna in [antenna1, antenna2]:
        for direction in [-1, 1]:
            multiplier = 1
            while True:
                antinode = (
                    antenna[0] + multiplier * direction * dx,
                    antenna[1] + multiplier * direction * dy,
                )
                if 0 <= antinode[0] < len(antenna_map) and 0 <= antinode[1] < len(
                    antenna_map[0]
                ):
                    antinodes.append(antinode)
                    multiplier += 1
                else:
                    break

    return antinodes


def main() -> None:
    with open("input.txt") as f:
        antenna_map = f.read().splitlines()

        antenna_dict = dict[str, list[tuple[int, int]]]()
        for row_index, row in enumerate(antenna_map):
            for col_index, char in enumerate(row):
                if char == ".":
                    continue

                try:
                    antenna_dict[char].append((row_index, col_index))
                except KeyError:
                    antenna_dict[char] = [(row_index, col_index)]

        antinodes = set[tuple[int, int]]()
        for _, antenna_positions in antenna_dict.items():
            for i in range(len(antenna_positions)):
                for j in range(i + 1, len(antenna_positions)):
                    antinodes |= set(
                        get_antinodes_part1(
                            antenna_map, antenna_positions[i], antenna_positions[j]
                        )
                    )

        print(f"Part 1: {len(antinodes)}")

        antinodes = set[tuple[int, int]]()
        for _, antenna_positions in antenna_dict.items():
            for i in range(len(antenna_positions)):
                for j in range(i + 1, len(antenna_positions)):
                    antinodes |= set(
                        get_antinodes_part2(
                            antenna_map, antenna_positions[i], antenna_positions[j]
                        )
                    )

        print(f"Part 2: {len(antinodes)}")


if __name__ == "__main__":
    main()
