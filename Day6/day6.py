#!/bin/env python

from enum import Enum


class Direction(Enum):
    N = (-1, 0)
    E = (0, 1)
    S = (1, 0)
    W = (0, -1)


def traverse_map(
    lab_map: list[list[str]], start_coords: tuple[int, int]
) -> tuple[bool, set[tuple[int, int]]]:
    facing = Direction.N
    guard_coords = start_coords
    visited = {(facing, guard_coords)}

    while True:
        next_guard_row = guard_coords[0] + facing.value[0]
        next_guard_col = guard_coords[1] + facing.value[1]

        if (
            next_guard_row < 0
            or next_guard_row >= len(lab_map)
            or next_guard_col < 0
            or next_guard_col >= len(lab_map[0])
        ):
            break

        if lab_map[next_guard_row][next_guard_col] == "#":
            match facing:
                case Direction.N:
                    facing = Direction.E
                case Direction.S:
                    facing = Direction.W
                case Direction.E:
                    facing = Direction.S
                case Direction.W:
                    facing = Direction.N
                case _:
                    raise Exception("Invalid facing direction")
            if (facing, guard_coords) in visited:
                return True, {v[1] for v in visited}
            visited.add((facing, guard_coords))
            continue

        guard_coords = (next_guard_row, next_guard_col)
        if (facing, guard_coords) in visited:
            return True, {v[1] for v in visited}
        visited.add((facing, guard_coords))

    return False, {v[1] for v in visited}


def main() -> None:
    with open("input.txt") as f:
        lab_map = [list(line) for line in f.read().splitlines()]

        start_coords = tuple[int, int]()
        for row, line in enumerate(lab_map):
            for col, char in enumerate(line):
                if char == "^":
                    start_coords = (row, col)

        _, visited_coords = traverse_map(lab_map, start_coords)

        print(f"Part 1: {len(visited_coords)}")

        num_of_possible_obstacles = 0
        for row, col in visited_coords:
            if (row, col) == start_coords:
                continue

            lab_map[row][col] = "#"
            is_loop, _ = traverse_map(lab_map, start_coords)
            lab_map[row][col] = "."

            if is_loop:
                num_of_possible_obstacles += 1

        print(f"Part 2: {num_of_possible_obstacles}")


if __name__ == "__main__":
    main()
