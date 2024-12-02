#!/bin/env python


def is_safe_pair(
    d1: int, d2: int, increasing: bool, first_pair: bool
) -> tuple[bool, bool, bool]:
    safe = True
    next_increasing = increasing
    next_first_pair = first_pair

    if first_pair:
        next_increasing = d1 < d2
        next_first_pair = False
    else:
        if (d1 < d2) != increasing:
            safe = False

    if d1 == d2 or abs(d1 - d2) > 3:
        safe = False

    return safe, next_increasing, next_first_pair


def is_safe_report(report: list[int], maximum_num_of_elements_removed: int = 0) -> bool:
    first_pair = True
    increasing = True
    safe_report = True
    num_of_elements_removed = 0

    i = 0
    while i < len(report) - 1:
        d1 = report[i]
        d2 = report[i + 1]
        safe, increasing, first_pair = is_safe_pair(d1, d2, increasing, first_pair)
        if not safe:
            if num_of_elements_removed == maximum_num_of_elements_removed:
                safe_report = False
                break

            if i == len(report) - 2:
                break

            d2 = report[i + 2]
            i += 1
            safe, increasing, first_pair = is_safe_pair(d1, d2, increasing, first_pair)
            if not safe:
                safe_report = False
                break
            else:
                num_of_elements_removed += 1

        i += 1

    return safe_report


def main() -> None:
    with open("input.txt") as f:
        data = [[int(n) for n in l.split(" ")] for l in f.readlines()]

        num_safe_reports = 0
        for l in data:
            safe_report = is_safe_report(l, 0)

            if safe_report:
                num_safe_reports += 1

        print(f"Part 1: {num_safe_reports}")

        num_safe_reports = 0
        for l in data:
            safe_report = is_safe_report(l, 1) or is_safe_report(l[::-1], 1)

            if safe_report:
                num_safe_reports += 1

        print(f"Part 2: {num_safe_reports}")


if __name__ == "__main__":
    main()
