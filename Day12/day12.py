#!/bin/env python


from collections import defaultdict


def find_connected_region(
    region_map: list[list[str]], visited_map: list[list[bool]], row: int, col: int
) -> list[tuple[int, int]]:
    region = list[tuple[int, int]]()
    region.append((row, col))
    visited_map[row][col] = True

    for drow, dcol in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        next_row, next_col = row + drow, col + dcol
        if (
            next_row < 0
            or next_row >= len(region_map)
            or next_col < 0
            or next_col >= len(region_map[0])
        ):
            continue

        if visited_map[next_row][next_col]:
            continue

        if region_map[next_row][next_col] == region_map[row][col]:
            region += find_connected_region(region_map, visited_map, next_row, next_col)

    return region


def find_perimeter_from_region(region: list[tuple[int, int]]) -> int:
    perimeter = 0
    for row, col in region:
        for drow, dcol in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if (row + drow, col + dcol) not in region:
                perimeter += 1

    return perimeter


def find_sides_from_region(region: list[tuple[int, int]]) -> int:
    sides = 0

    sorted_by_row = defaultdict(list[int])
    for row, col in region:
        sorted_by_row[row].append(col)
    for row in sorted_by_row:
        sorted_by_row[row].sort()

    edge_by_row = defaultdict(list[int])
    for row in sorted_by_row:
        edge_by_row[row].append(sorted_by_row[row][0])
        for i in range(1, len(sorted_by_row[row])):
            if sorted_by_row[row][i] - sorted_by_row[row][i - 1] != 1:
                edge_by_row[row].append(sorted_by_row[row][i - 1])
                edge_by_row[row].append(sorted_by_row[row][i])
        edge_by_row[row].append(sorted_by_row[row][-1])

    start_end_pair_by_row = defaultdict(list[tuple[int, int]])
    for row in edge_by_row:
        for i in range(0, len(edge_by_row[row]), 2):
          start_end_pair_by_row[row].append((edge_by_row[row][i], edge_by_row[row][i + 1]))
    sorted_start_end_pair_by_row = dict(sorted(start_end_pair_by_row.items()))

    last_row_starts = set[int]()
    last_row_ends = set[int]()
    for row, pairs in sorted_start_end_pair_by_row.items():
        for start, end in pairs:
            if start not in last_row_starts:
                sides += 1
            if end not in last_row_ends:
                sides += 1

        last_row_starts = {pair[0] for pair in pairs}
        last_row_ends = {pair[1] for pair in pairs}

    sorted_by_col = defaultdict(list[int])
    for row, col in region:
        sorted_by_col[col].append(row)
    for col in sorted_by_col:
        sorted_by_col[col].sort()

    edge_by_col = defaultdict(list[int])
    for col in sorted_by_col:
        edge_by_col[col].append(sorted_by_col[col][0])
        for i in range(1, len(sorted_by_col[col])):
            if sorted_by_col[col][i] - sorted_by_col[col][i - 1] != 1:
                edge_by_col[col].append(sorted_by_col[col][i - 1])
                edge_by_col[col].append(sorted_by_col[col][i])
        edge_by_col[col].append(sorted_by_col[col][-1])

    start_end_pair_by_col = defaultdict(list[tuple[int, int]])
    for col in edge_by_col:
        for i in range(0, len(edge_by_col[col]), 2):
          start_end_pair_by_col[col].append((edge_by_col[col][i], edge_by_col[col][i + 1]))
    sorted_start_end_pair_by_col = dict(sorted(start_end_pair_by_col.items()))

    last_col_starts = set[int]()
    last_col_ends = set[int]()
    for col, pairs in sorted_start_end_pair_by_col.items():
        for start, end in pairs:
            if start not in last_col_starts:
                sides += 1
            if end not in last_col_ends:
                sides += 1

        last_col_starts = {pair[0] for pair in pairs}
        last_col_ends = {pair[1] for pair in pairs}

    return sides


def main() -> None:
    with open("input.txt") as f:
        region_map = [line.strip() for line in f.readlines()]

        visited_map = [
            [False for _ in range(len(region_map[0]))] for _ in range(len(region_map))
        ]

        total_price_part1 = 0
        total_price_part2 = 0
        for row in range(len(region_map)):
            for col in range(len(region_map[0])):
                if visited_map[row][col]:
                    continue

                region = find_connected_region(region_map, visited_map, row, col)
                total_price_part1 += find_perimeter_from_region(region) * len(region)
                total_price_part2 += find_sides_from_region(region) * len(region)

        print(f"Part 1: {total_price_part1}")
        print(f"Part 2: {total_price_part2}")


if __name__ == "__main__":
    main()
