#!/bin/env python

import math

from typing import Optional


Point = tuple[int, int]


def cost_backtrace(
    parent: dict[Point, Point], current: Optional[Point]
) -> list[Point]:
    trace = list[Point]()
    while current:
        trace.insert(0, current)
        current = parent.get(current)

    return trace


def dijkstra(
    race_track: list[list[str]], start: Point, end: Point
) -> tuple[list[Point], dict[Point, int]]:
    pending = {start}
    parent = dict[Point, Point]()
    node_cost = {start: 0}

    while len(pending) > 0:
        curr_node = min(pending, key=lambda t: node_cost[t])

        if curr_node == end:
            break

        pending.remove(curr_node)

        for drow, dcol in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (curr_node[0] + drow, curr_node[1] + dcol)

            if race_track[neighbor[0]][neighbor[1]] == "#":
                continue

            new_cost = node_cost[curr_node] + 1
            if new_cost >= node_cost.get(neighbor, math.inf):
                continue

            parent[neighbor] = curr_node
            node_cost[neighbor] = new_cost

            pending.add(neighbor)

    trace = cost_backtrace(parent, end)

    return trace, node_cost


def main() -> None:
    with open("input.txt") as f:
        race_track = [list(line) for line in f.read().strip().splitlines()]

        for row, cols in enumerate(race_track):
            for col, cell in enumerate(cols):
                match cell:
                    case "S":
                        start = (row, col)
                    case "E":
                        end = (row, col)
                    case _:
                        pass

        possible_cheats = list[Point]()
        for row, cols in enumerate(race_track):
            for col, cell in enumerate(cols):
                if cell == "#":
                    possible = False
                    for drow, dcol in [(0, 1), (1, 0)]:
                        new_row1, new_col1 = (
                            row + drow,
                            col + dcol,
                        )
                        new_row2, new_col2 = (
                            row - drow,
                            col - dcol,
                        )

                        if (
                            new_row1 < 0
                            or new_row1 > len(race_track) - 1
                            or new_col1 < 0
                            or new_col1 > len(race_track[0]) - 1
                            or new_row2 < 0
                            or new_row2 > len(race_track) - 1
                            or new_col2 < 0
                            or new_col2 > len(race_track[0]) - 1
                        ):
                            continue

                        if (
                            race_track[new_row1][new_col1] == "#"
                            or race_track[new_row2][new_col2] == "#"
                        ):
                            continue

                        possible = True

                    if possible:
                        possible_cheats.append((row, col))

        base_line_trace, base_line_time = dijkstra(race_track, start, end)

        num_of_cheats_save_gt_100 = 0
        for cheat_row, cheat_col in possible_cheats:
            race_track[cheat_row][cheat_col] = "."
            _, cheat_time = dijkstra(race_track, start, end)
            race_track[cheat_row][cheat_col] = "#"

            if base_line_time[end] - cheat_time[end] >= 100:
                num_of_cheats_save_gt_100 += 1

        print(f"Part 1: {num_of_cheats_save_gt_100}")

        num_of_cheats_save_gt_100 = 0
        for i in range(len(base_line_trace)):
            for j in range(i + 1, len(base_line_trace)):
                s = base_line_trace[i]
                e = base_line_trace[j]

                manhatten_distance = abs(s[0] - e[0]) + abs(s[1] - e[1])

                if manhatten_distance > 20:
                    continue

                if base_line_time[e] - base_line_time[s] - manhatten_distance >= 100:
                    num_of_cheats_save_gt_100 += 1

        print(f"Part 2: {num_of_cheats_save_gt_100}")


if __name__ == "__main__":
    main()
