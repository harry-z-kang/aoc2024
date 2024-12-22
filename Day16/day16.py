#!/bin/env python

import math

from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class Point:
    row: int
    col: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.row + other.row, self.col + other.col)

    def __hash__(self):
        return hash((self.row, self.col))


class Direction(Enum):
    RIGHT = Point(0, 1)
    DOWN = Point(1, 0)
    LEFT = Point(0, -1)
    UP = Point(-1, 0)

    def get_possible_next_directions(self) -> list[tuple["Direction", int]]:
        match self:
            case Direction.UP:
                return [
                    (Direction.LEFT, 1000),
                    (Direction.UP, 0),
                    (Direction.RIGHT, 1000),
                    # (Direction.DOWN, 2000),
                ]
            case Direction.RIGHT:
                return [
                    (Direction.UP, 1000),
                    (Direction.RIGHT, 0),
                    (Direction.DOWN, 1000),
                    # (Direction.LEFT, 2000),
                ]
            case Direction.DOWN:
                return [
                    (Direction.RIGHT, 1000),
                    (Direction.DOWN, 0),
                    (Direction.LEFT, 1000),
                    # (Direction.UP, 2000),
                ]
            case Direction.LEFT:
                return [
                    (Direction.DOWN, 1000),
                    (Direction.LEFT, 0),
                    (Direction.UP, 1000),
                    # (Direction.RIGHT, 2000),
                ]
            case _:
                raise ValueError("Invalid direction")


@dataclass
class Node:
    point: Point
    direction: Direction

    def __hash__(self):
        return hash((self.point, self.direction))


def get_points_valid_on_at_least_one_trace(
    parent: dict[Node, Node], node_cost: dict[Node, int], curr_node: Optional[Node]
) -> set[Point]:
    last_direction = curr_node.direction
    points = {curr_node.point}

    while curr_node := parent.get(curr_node):
        points.add(curr_node.point)

        for direction, _ in curr_node.direction.get_possible_next_directions():
            if direction == curr_node.direction:
                continue

            possible_node = Node(curr_node.point, direction)

            if (
                last_direction != curr_node.direction
                and (node_cost.get(possible_node, 0) - node_cost[curr_node]) == 1000
            ):
                points |= get_points_valid_on_at_least_one_trace(
                    parent, node_cost, parent.get(possible_node)
                )

        last_direction = curr_node.direction

    return points


def dijkstra(maze: list[list[str]], start: Node, end: Point) -> tuple[set[Point], int]:
    pending = {start}
    parent = dict[Node, Node]()
    node_cost = {start: 0}

    while len(pending) > 0:
        curr_node = min(pending, key=lambda t: node_cost[t])

        if curr_node.point == end:
            return (
                get_points_valid_on_at_least_one_trace(parent, node_cost, curr_node),
                node_cost[curr_node],
            )

        pending.remove(curr_node)

        for (
            direction,
            turning_cost,
        ) in curr_node.direction.get_possible_next_directions():
            neighbor = Node(curr_node.point + direction.value, direction)

            if maze[neighbor.point.row][neighbor.point.col] == "#":
                continue

            new_cost = node_cost[curr_node] + turning_cost + 1
            if new_cost >= node_cost.get(neighbor, math.inf):
                continue

            parent[neighbor] = curr_node
            node_cost[neighbor] = new_cost

            pending.add(neighbor)


def main():
    with open("input.txt") as f:
        maze = [list(row) for row in f.read().strip().splitlines()]

        for row, cols in enumerate(maze):
            for col, cell in enumerate(cols):
                if cell == "S":
                    start = Node(Point(row, col), Direction.RIGHT)
                elif cell == "E":
                    end = Point(row, col)

        num_of_points, shortest_path_cost = dijkstra(maze, start, end)

        print(f"Part 1: {shortest_path_cost}")
        print(f"Part 2: {len(num_of_points)}")


if __name__ == "__main__":
    main()
