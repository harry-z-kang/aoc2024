#!/bin/env python


from typing import Callable
from multiprocessing import Process, Manager


def multiply(a: int, b: int) -> int:
    return a * b


def add(a: int, b: int) -> int:
    return a + b


def concatenate(a: int, b: int) -> int:
    return int(str(a) + str(b))


def _check_prompt(
    goal: int,
    operands: list[int],
    opeator_choices: list[Callable[[int, int], int]],
) -> bool:
    if len(operands) == 1:
        return operands[0] == goal

    if operands[0] > goal:
        return False

    if operands[0] == goal:
        return len(operands) == 2 and operands[1] in [0, 1]

    return any(
        [
            _check_prompt(
                goal,
                [operator(operands[0], operands[1])] + operands[2:],
                opeator_choices,
            )
            for operator in opeator_choices
        ]
    )


def check_prompt(
    goal: int,
    operands: list[int],
    opeator_choices: list[Callable[[int, int], int]],
    possible_array: list[bool],
    index: int,
) -> None:
    possible_array[index] = _check_prompt(goal, operands, opeator_choices)


def get_total_calibration_result(
    prompts: list[tuple[int, list[int]]],
    opeator_choices: list[Callable[[int, int], int]],
) -> int:
    possible = Manager().list([False for _ in prompts])

    processes = list[Process]()
    for i, (goal, operands) in enumerate(prompts):
        processes.append(
            Process(
                target=check_prompt, args=(goal, operands, opeator_choices, possible, i)
            )
        )

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    return sum([possible * goal for possible, (goal, _) in zip(possible, prompts)])


def main() -> None:
    with open("input.txt") as f:
        prompts = [
            (int(line.split(": ")[0]), [int(n) for n in line.split(": ")[1].split(" ")])
            for line in f.read().splitlines()
        ]

        print(f"Part 1: {get_total_calibration_result(prompts, [add, multiply])}")
        print(
            f"Part 2: {get_total_calibration_result(prompts, [add, concatenate, multiply])}"
        )


if __name__ == "__main__":
    main()
