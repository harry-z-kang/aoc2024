#!/bin/env python

from enum import Enum


class Direction(Enum):
    N = (-1, 0)
    S = (1, 0)
    E = (0, 1)
    W = (0, -1)
    NE = (-1, 1)
    NW = (-1, -1)
    SE = (1, 1)
    SW = (1, -1)


X_MAS_DIRECTION_MAPPING = {
    Direction.NE: [(Direction.E, Direction.NW), (Direction.N, Direction.SE)],
    Direction.NW: [(Direction.W, Direction.NE), (Direction.N, Direction.SW)],
    Direction.SE: [(Direction.E, Direction.SW), (Direction.S, Direction.NE)],
    Direction.SW: [(Direction.W, Direction.SE), (Direction.S, Direction.NW)],
}


def search_word_in_direction(
    start_row: int,
    start_col: int,
    word: str,
    direction: Direction,
    word_search_map: list,
) -> bool:
    if (
        start_row < 0
        or start_row >= len(word_search_map)
        or start_col < 0
        or start_col >= len(word_search_map[0])
    ):
        return False

    assert word_search_map[start_row][start_col] == word[0]

    for i, char in enumerate(word):
        if i == 0:
            continue

        row = start_row + i * direction.value[0]
        col = start_col + i * direction.value[1]

        if (
            row < 0
            or row >= len(word_search_map)
            or col < 0
            or col >= len(word_search_map[0])
        ):
            return False

        if word_search_map[row][col] != char:
            return False

    return True


def search_word(
    start_row: int, start_col: int, word: str, word_search_map: list
) -> list[Direction]:
    occurance_directions = list[Direction]()

    for direction in Direction:
        if search_word_in_direction(
            start_row, start_col, word, direction, word_search_map
        ):
            occurance_directions.append(direction)

    return occurance_directions


def main() -> None:
    with open("input.txt") as f:
        word_search_map = [l.strip() for l in f.readlines()]

        num_of_occurrence = 0
        for row in range(len(word_search_map)):
            for col in range(len(word_search_map[0])):
                if word_search_map[row][col] != "X":
                    continue

                num_of_occurrence += len(search_word(row, col, "XMAS", word_search_map))

        print(f"Part 1: {num_of_occurrence}")

        num_of_occurrence = 0
        for row in range(len(word_search_map)):
            for col in range(len(word_search_map[0])):
                if word_search_map[row][col] != "M":
                    continue

                for direction in search_word(row, col, "MAS", word_search_map):
                    if direction not in X_MAS_DIRECTION_MAPPING:
                        continue

                    for cross_start_direction, cross_direction in X_MAS_DIRECTION_MAPPING[direction]:
                        cross_start_row = row + 2 * cross_start_direction.value[0]
                        cross_start_col = col + 2 * cross_start_direction.value[1]

                        if word_search_map[cross_start_row][cross_start_col] != "M":
                            continue

                        if search_word_in_direction(cross_start_row, cross_start_col, "MAS", cross_direction, word_search_map):
                            num_of_occurrence += 1

        assert num_of_occurrence % 2 == 0

        print(f"Part 2: {num_of_occurrence // 2}")


if __name__ == "__main__":
    main()
