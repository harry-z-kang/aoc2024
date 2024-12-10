#!/bin/env python


from collections import deque
from typing import Optional


def part1() -> None:
    with open("input.txt") as f:
        files = deque[tuple[int, int]]()
        spaces = deque[int]()

        file_system = list[Optional[int]]()

        position = 0
        file_id = 0
        for i, num in enumerate([int(c) for c in f.read().strip()]):
            if i % 2 == 0:
                for _ in range(num):
                    files.append((position, file_id))
                    file_system.append(file_id)
                    position += 1
                file_id += 1
            else:
                for _ in range(num):
                    spaces.append(position)
                    file_system.append(None)
                    position += 1

        file_system_size = len(files)

        while files[-1][0] > spaces[0]:
            file_system[spaces[0]] = files[-1][1]
            files.pop()
            spaces.popleft()

        print(
            f"Part 1: {sum([i * num for i, num in enumerate(file_system[:file_system_size]) if num != None])}"
        )


def part2() -> None:
    with open("input.txt") as f:
        files = deque[tuple[int, int, int]]()
        spaces = deque[tuple[int, int]]()

        file_system = list[Optional[int]]()

        position = 0
        file_id = 0
        for i, num in enumerate([int(c) for c in f.read().strip()]):
            if i % 2 == 0:
                files.append((position, num, file_id))
                for _ in range(num):
                    file_system.append(file_id)
                    position += 1
                file_id += 1
            else:
                spaces.append((position, num))
                for _ in range(num):
                    file_system.append(None)
                    position += 1

        for file_position, file_size, file_id in reversed(files):
            for i, (space_position, space_size) in enumerate(spaces):
                if space_position < file_position and space_size >= file_size:
                    for swap_i in range(file_size):
                        file_system[space_position + swap_i] = file_id
                        file_system[file_position + swap_i] = None
                    spaces[i] = (space_position + file_size, space_size - file_size)
                    break

        print(
            f"Part 2: {sum([i * num for i, num in enumerate(file_system) if num != None])}"
        )


def main() -> None:
    part1()
    part2()


if __name__ == "__main__":
    main()
