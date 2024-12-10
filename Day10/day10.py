#!/bin/env python


def get_reacheable_highest(
    topology: list[list[int]], position: tuple[int, int]
) -> set[tuple[int, int]]:
    row, col = position

    if topology[row][col] == 9:
        return {position}

    reacheable_heights = set[tuple[int, int]]()
    for drow, dcol in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        next_row, next_col = position[0] + drow, position[1] + dcol
        if (
            next_row < 0
            or next_row >= len(topology[0])
            or next_col < 0
            or next_col >= len(topology)
        ):
            continue

        if topology[next_row][next_col] - topology[row][col] == 1:
            reacheable_heights |= get_reacheable_highest(topology, (next_row, next_col))

    return reacheable_heights


def find_trail(topology: list[list[int]], position: tuple[int, int]) -> list[list[tuple[int, int]]]:
    row, col = position

    if topology[row][col] == 9:
        return [[position]]

    trails = list[list[tuple[int, int]]]()
    for drow, dcol in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        next_row, next_col = position[0] + drow, position[1] + dcol
        if (
            next_row < 0
            or next_row >= len(topology[0])
            or next_col < 0
            or next_col >= len(topology)
        ):
            continue

        if topology[next_row][next_col] - topology[row][col] == 1:
            for trail in find_trail(topology, (next_row, next_col)):
                trails.append([position] + trail)

    return trails

def main() -> None:
    with open("input.txt") as f:
        topology = [[int(height) for height in line] for line in f.read().splitlines()]

        trailheads = list[tuple[int, int]]()
        for row, heights in enumerate(topology):
            for col, height in enumerate(heights):
                if height == 0:
                    trailheads.append((row, col))

        print(f"Part 1: {sum([len(get_reacheable_highest(topology, trailhead)) for trailhead in trailheads])}")
        print(f"Part 2: {sum([len(find_trail(topology, trailhead)) for trailhead in trailheads])}")


if __name__ == "__main__":
    main()
