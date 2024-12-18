#!/bin/env python

import math


BOARD_SIZE = 71
TRUNCATE_INDEX = 1024


Point = tuple[int, int]


def cost_heuristic(point: Point, end: Point) -> float:
    return math.sqrt((point[0] - end[0]) ** 2 + (point[1] - end[1]) ** 2)


def a_star(byte_positions: list[Point], truncate_index: int) -> int:
    start = (0, 0)
    end = (BOARD_SIZE - 1, BOARD_SIZE - 1)

    pending = {start}
    parent = dict[Point, Point]()
    node_cost = {start: 0.0}
    total_cost = {start: cost_heuristic(start, end)}

    while len(pending) > 0:
        curr_node = min(pending, key=lambda t: total_cost[t])

        if curr_node == end:
            break

        pending.remove(curr_node)

        for drow, dcol in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (curr_node[0] + drow, curr_node[1] + dcol)

            if (
                neighbor[0] < 0
                or neighbor[1] < 0
                or neighbor[0] > BOARD_SIZE - 1
                or neighbor[1] > BOARD_SIZE - 1
            ):
                continue

            if neighbor in byte_positions[:truncate_index]:
                continue

            new_cost = node_cost[curr_node] + 1
            if new_cost >= node_cost.get(neighbor, math.inf):
                continue

            parent[neighbor] = curr_node
            node_cost[neighbor] = new_cost
            total_cost[neighbor] = new_cost + cost_heuristic(neighbor, end)

            pending.add(neighbor)

    return int(node_cost[end])


def main() -> None:
    with open("input.txt") as f:
        byte_positions = [
            (int(b.split(",")[1]), int(b.split(",")[0]))
            for b in f.read().strip().splitlines()
        ]

        print(f"Part 1: {a_star(byte_positions, TRUNCATE_INDEX)}")

        for i in range(TRUNCATE_INDEX, len(byte_positions) + 1):
            print(f"Checking {i}")
            try:
                a_star(byte_positions, i)
            except KeyError:
                print(f"Part 2: {byte_positions[i - 1][1]},{byte_positions[i - 1][0]}")
                break


if __name__ == "__main__":
    main()
