#!/bin/env python

from copy import deepcopy


SYMBOL_DIRECTION_MAPPING = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}


def part1(box_map: list[list[str]], moves: list[str]) -> int:
    for row, cols in enumerate(box_map):
        for col, cell in enumerate(cols):
            if cell == "@":
                start = (row, col)
                break

    for move in moves:
        moveable_objects = find_moveable_objects_part1(
            box_map,
            SYMBOL_DIRECTION_MAPPING[move],
            start,
        )

        if len(moveable_objects) == 0:
            continue

        drow, dcol = SYMBOL_DIRECTION_MAPPING[move]
        box_map[moveable_objects[-1][0] + drow][moveable_objects[-1][1] + dcol] = "O"
        box_map[moveable_objects[0][0]][moveable_objects[0][1]] = "."
        box_map[moveable_objects[0][0] + drow][moveable_objects[0][1] + dcol] = "@"

        start = (moveable_objects[0][0] + drow, moveable_objects[0][1] + dcol)

    total_gps_coords = 0
    for row, cols in enumerate(box_map):
        for col, cell in enumerate(cols):
            if cell == "O":
                total_gps_coords += 100 * row + col

    return total_gps_coords


def find_moveable_objects_part1(
    box_map: list[list[str]],
    direction: tuple[int, int],
    starting_position: tuple[int, int],
) -> list[tuple[int, int]]:
    moveable_objects = list[tuple[int, int]]()
    moveable_objects.append(starting_position)

    curr_row, curr_col = starting_position
    while True:
        curr_row += direction[0]
        curr_col += direction[1]

        if box_map[curr_row][curr_col] == "#":
            return []

        if box_map[curr_row][curr_col] == ".":
            break

        if box_map[curr_row][curr_col] == "O":
            moveable_objects.append((curr_row, curr_col))

    return moveable_objects


def part2(box_map: list[list[str]], moves: list[str]) -> int:
    box_map_expanded = list[list[str]]()
    for row in box_map:
        expanded_row = list[str]()
        for cell in row:
            match cell:
                case "#":
                    expanded_row.extend(["#", "#"])
                case ".":
                    expanded_row.extend([".", "."])
                case "@":
                    expanded_row.extend(["@", "."])
                case "O":
                    expanded_row.extend(["[", "]"])
        box_map_expanded.append(expanded_row)

    for row, cols in enumerate(box_map_expanded):
        for col, cell in enumerate(cols):
            if cell == "@":
                start = (row, col)
                break

    for move in moves:
        match move:
            case "<" | ">":
                moveable_objects = find_moveable_objects_row_part2(
                    box_map_expanded,
                    SYMBOL_DIRECTION_MAPPING[move],
                    start,
                )
            case "^" | "v":
                moveable_objects = find_moveable_objects_col_part2(
                    box_map_expanded,
                    SYMBOL_DIRECTION_MAPPING[move],
                    start,
                )
            case _:
                raise ValueError(f"Invalid Move: {move}")

        if len(moveable_objects) == 0:
            continue

        drow, dcol = SYMBOL_DIRECTION_MAPPING[move]
        original_cell = dict[tuple[int, int], str]()
        for obj in moveable_objects:
            original_cell[obj] = box_map_expanded[obj[0]][obj[1]]
        for obj in moveable_objects:
            box_map_expanded[obj[0]][obj[1]] = "."
        for obj in moveable_objects:
            box_map_expanded[obj[0] + drow][obj[1] + dcol] = original_cell[obj]

        start = (moveable_objects[0][0] + drow, moveable_objects[0][1] + dcol)

    total_gps_coords = 0
    for row, cols in enumerate(box_map_expanded):
        for col, cell in enumerate(cols):
            if cell == "[":
                total_gps_coords += 100 * row + col

    return total_gps_coords


def find_moveable_objects_row_part2(
    box_map: list[list[str]],
    direction: tuple[int, int],
    starting_position: tuple[int, int],
) -> list[tuple[int, int]]:
    moveable_objects = list[tuple[int, int]]()
    moveable_objects.append(starting_position)

    curr_row, curr_col = starting_position
    while True:
        curr_row += direction[0]
        curr_col += direction[1]

        match box_map[curr_row][curr_col]:
            case "#":
                return []
            case ".":
                break
            case "[" | "]":
                moveable_objects.append((curr_row, curr_col))

    return moveable_objects


def find_moveable_objects_col_part2(
    box_map: list[list[str]],
    direction: tuple[int, int],
    starting_position: tuple[int, int],
) -> list[tuple[int, int]]:
    moveable_objects = list[tuple[int, int]]()
    moveable_objects.append(starting_position)

    curr_row, curr_col = starting_position
    while True:
        curr_row += direction[0]
        curr_col += direction[1]

        match box_map[curr_row][curr_col]:
            case "#":
                return []
            case ".":
                break
            case "[":
                right_box_subsequent_moveable_objects = find_moveable_objects_col_part2(
                    box_map, direction, (curr_row, curr_col + 1)
                )
                left_box_subsequent_moveable_objects = find_moveable_objects_col_part2(
                    box_map, direction, (curr_row, curr_col)
                )
            case "]":
                right_box_subsequent_moveable_objects = find_moveable_objects_col_part2(
                    box_map, direction, (curr_row, curr_col - 1)
                )
                left_box_subsequent_moveable_objects = find_moveable_objects_col_part2(
                    box_map, direction, (curr_row, curr_col)
                )

        if len(right_box_subsequent_moveable_objects) == 0 or len(left_box_subsequent_moveable_objects) == 0:
            return []
        else:
            moveable_objects += right_box_subsequent_moveable_objects
            moveable_objects += left_box_subsequent_moveable_objects

    return moveable_objects


def main() -> None:
    with open("input.txt") as f:
        box_map_raw, moves_raw = f.read().split("\n\n")

        box_map = [list(row) for row in box_map_raw.splitlines()]
        moves = "".join([line.strip() for line in moves_raw])

        print(f"Part 1: {part1(deepcopy(box_map), moves)}")
        print(f"Part 2: {part2(deepcopy(box_map), moves)}")


if __name__ == "__main__":
    main()
