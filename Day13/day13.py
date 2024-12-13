#!/bin/env python

from dataclasses import dataclass


@dataclass
class Machine:
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]

    @property
    def num_presses(self) -> tuple[int, int]:
        return (
            (self.prize[0] * self.button_b[1] - self.prize[1] * self.button_b[0])
            / (
                self.button_a[0] * self.button_b[1]
                - self.button_a[1] * self.button_b[0]
            ),
            (self.prize[1] * self.button_a[0] - self.prize[0] * self.button_a[1])
            / (
                self.button_a[0] * self.button_b[1]
                - self.button_a[1] * self.button_b[0]
            ),
        )


def main() -> None:
    with open("input.txt") as f:
        machines_raw = f.read().split("\n\n")

        machines = list[Machine]()
        for machine_raw in machines_raw:
            button_a_raw, button_b_raw, prize_raw = machine_raw.splitlines()
            button_a = tuple(
                [
                    int(distance.split("+")[1])
                    for distance in button_a_raw.split(": ")[1].split(", ")
                ]
            )
            button_b = tuple(
                [
                    int(distance.split("+")[1])
                    for distance in button_b_raw.split(": ")[1].split(", ")
                ]
            )
            prize = tuple(
                [
                    int(distance.split("=")[1])
                    for distance in prize_raw.split(": ")[1].split(", ")
                ]
            )
            machines.append(Machine(button_a, button_b, prize))

        total_prize = 0
        for machine in machines:
            num_presses_a, num_presses_b = machine.num_presses

            if num_presses_a.is_integer() and num_presses_b.is_integer():
                total_prize += int(num_presses_a) * 3 + int(num_presses_b)

        print(f"Part 1: {total_prize}")

        total_prize = 0
        for machine in machines:
            machine.prize = (
                machine.prize[0] + 10_000_000_000_000,
                machine.prize[1] + 10_000_000_000_000,
            )

            num_presses_a, num_presses_b = machine.num_presses

            if num_presses_a.is_integer() and num_presses_b.is_integer():
                total_prize += int(num_presses_a) * 3 + int(num_presses_b)

        print(f"Part 2: {total_prize}")


if __name__ == "__main__":
    main()
