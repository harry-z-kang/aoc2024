#!/bin/env python

from functools import cache
from itertools import product

NUMERIC = "789456123 0A"
DIRECTIONAL = " ^A<v>"


@cache
def get_robot_inputs(keymap: str) -> dict[tuple[str, str], list[str]]:
    coords = {
        char: (col, row)
        for row, cols in enumerate(keymap[i : i + 3] for i in range(0, len(keymap), 3))
        for col, char in enumerate(cols)
    }

    path_map = dict[tuple[str, str], list[str]]()

    for start, end in product((char for char in keymap if char != " "), repeat=2):
        if start == end:
            path_map[start, end] = [""]
            continue

        (start_col, start_row), (end_col, end_row) = coords[start], coords[end]
        dcol, drow = end_col - start_col, end_row - start_row

        moves_col = [">", "<"][dcol < 0] * abs(dcol)
        moves_row = ["v", "^"][drow < 0] * abs(drow)

        # YX Routing
        if coords[" "] == (end_col, start_row):
            path_map[start, end] = [moves_row + moves_col]
        # XY Routing
        elif coords[" "] == (start_col, end_row):
            path_map[start, end] = [moves_col + moves_row]
        else:
            path_map[start, end] = [moves_col + moves_row, moves_row + moves_col]

    return path_map


@cache
def get_last_level_min_num_of_presses(code: str, depth: int, keypad: str = NUMERIC) -> int:
    if depth == 1:
        return len(code)

    key_paths = get_robot_inputs(keypad)
    return sum(
        min(get_last_level_min_num_of_presses(f"{path}A", depth - 1, DIRECTIONAL) for path in key_paths[pair])
        for pair in zip(f"A{code}", code)
    )


def main() -> None:
    with open("input.txt") as f:
        codes = [line.strip() for line in f.readlines()]

    print(f"Part 1: {sum(get_last_level_min_num_of_presses(code, 4) * int(code[:-1]) for code in codes)}")
    print(f"Part 2: {sum(get_last_level_min_num_of_presses(code, 27) * int(code[:-1]) for code in codes)}")


if __name__ == "__main__":
    main()
