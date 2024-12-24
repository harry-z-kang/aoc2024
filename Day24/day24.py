#!/bin/env python

from dataclasses import dataclass
from enum import StrEnum


class Op(StrEnum):
    XOR = "XOR"
    AND = "AND"
    OR = "OR"

    def __lt__(self, other: "Op") -> bool:
        return (
            self == Op.XOR
            and other in [Op.AND, Op.OR]
            or (self == Op.AND and other == Op.OR)
        )


@dataclass
class Operation:
    operand_0: str
    operand_1: str
    operand_2: str
    operator: Op

    def __str__(self):
        return f"{self.operand_0} {self.operator} {self.operand_1} -> {self.operand_2}"


def get_number(values: dict[str, int], operand: str) -> int:
    return int(
        "".join(
            [
                str(pair[1])
                for pair in sorted(
                    {k: v for k, v in values.items() if k[0] == operand}.items(),
                    reverse=True,
                )
            ]
        ),
        base=2,
    )


def main() -> None:
    with open("input.txt") as f:
        initial_values, operations_raw = f.read().strip().split("\n\n")

        values = dict[str, int]()
        for line in initial_values.splitlines():
            name, initial_value = line.split(": ")
            values[name] = int(initial_value)

        operations = list[Operation]()
        for op in operations_raw.splitlines():
            op_str, dst = op.split(" -> ")
            operand_0, op, operand_1 = op_str.split(" ")
            if operand_0[0] == "y" and operand_1[0] == "x":
                operations.append(Operation(operand_1, operand_0, dst, Op(op)))
            else:
                operations.append(Operation(operand_0, operand_1, dst, Op(op)))

        settled = [False] * len(operations)
        index = 0
        while not all(settled):
            operation = operations[index]

            try:
                match operation.operator:
                    case Op.AND:
                        values[operation.operand_2] = (
                            values[operation.operand_0] & values[operation.operand_1]
                        )
                    case Op.OR:
                        values[operation.operand_2] = (
                            values[operation.operand_0] | values[operation.operand_1]
                        )
                    case Op.XOR:
                        values[operation.operand_2] = (
                            values[operation.operand_0] ^ values[operation.operand_1]
                        )
                    case _:
                        raise ValueError(f"Unknown operation: {op}")
                settled[index] = True
            except KeyError:
                pass

            index = (index + 1) % len(operations)

        print(f"Part 1: {get_number(values, "z")}")

        operations.sort(key=lambda op: op.operator)

        correct_sum = get_number(values, "x") + get_number(values, "y")

        print(bin(get_number(values, "z")))
        print(bin(correct_sum))

        output_in_questions = list[str]()
        for index, (test_val, golden_val) in enumerate(
            zip(bin(get_number(values, "z"))[2:][::-1], bin(correct_sum)[2:][::-1])
        ):
            if test_val != golden_val:
                output_in_questions.append(f"z{index:02d}")

        print(output_in_questions)

        # For Part 2, I did not use an algorithm to solve the problem.
        # The first step is to find the output that does not align with the
        # golden value. The input is trying to simulate a full ripple adder
        # circuit where a simple schematic is the following:
        # sn = xn XOR yn;
        # an = xn AND yn;
        # hn = sn AND cn-1;
        # cn = an OR hn;
        # zn = sn XOR cn-1;
        # Basically, the operation that results in zn has to be out of an XOR
        # Op. If you start from the least significant bit that has miss-alignment
        # and work your way up, you can find the correct value for the output.
        # The correct answer is "gsd,kth,qnf,tbt,vpm,z12,z26,z32"


if __name__ == "__main__":
    main()
