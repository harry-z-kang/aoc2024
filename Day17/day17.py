#!/bin/env python


def combo(register_a: int, register_b: int, register_c: int, operand: int) -> int:
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return register_a
        case 5:
            return register_b
        case 6:
            return register_c
        case _:
            raise ValueError(f"Invalid operand: {operand}")


def run_program(
    program: list[tuple[int, int]], register_a: int, register_b: int, register_c: int
) -> str:
    program_counter = 0
    output = list[int]()
    while program_counter < len(program):
        opcode = program[program_counter][0]
        operand = program[program_counter][1]

        match opcode:
            case 0:
                register_a >>= combo(register_a, register_b, register_c, operand)
            case 1:
                register_b ^= operand
            case 2:
                register_b = combo(register_a, register_b, register_c, operand) & 0x7
            case 3:
                if register_a != 0:
                    program_counter = operand
                    continue
            case 4:
                register_b ^= register_c
            case 5:
                output.append(combo(register_a, register_b, register_c, operand) & 0x7)
            case 6:
                register_b = register_a >> combo(
                    register_a, register_b, register_c, operand
                )
            case 7:
                register_c = register_a >> combo(
                    register_a, register_b, register_c, operand
                )
            case _:
                raise ValueError(f"Invalid opcode: {opcode}")

        program_counter += 1

    return ",".join([str(n) for n in output])


def main() -> None:
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

        register_a = int(lines[0].split(": ")[-1])
        register_b = int(lines[1].split(": ")[-1])
        register_c = int(lines[2].split(": ")[-1])

        program_raw = [int(n) for n in lines[4].split(": ")[-1].split(",")]
        program = list[tuple[int, int]]()
        for i in range(0, len(program_raw), 2):
            program.append((program_raw[i], program_raw[i + 1]))

        print(f"Part 1: {run_program(program, register_a, register_b, register_c)}")

        # First, Burte Force the first couple of digits
        # in this case, I was able to figure out that the lower digits has to be 0o33267275
        # From there just brute force the rest
        # Another optimization is that from examining the program, we can see that the Register A
        # Value is being shifted right by 3, if we want 16 outputs, the number needs to be 48 bits
        for register_a in range(0o4000242133267275, 1 << (len(program) * 2 * 3), 0o100_000_000):
            output = run_program(program, register_a, 0, 0)
            if output == lines[4].split(": ")[-1]:
                print(oct(register_a), output)

        print(f"Part 2: {register_a}")


if __name__ == "__main__":
    main()
