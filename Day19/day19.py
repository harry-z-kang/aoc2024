#!/bin/env python


from collections import defaultdict

PATTERN_CACHE = dict[str, bool]()
PATTERN_TRACE_CACHE = dict[str, list[list[str]]]()


def is_pattern_possible(patterns: dict[str, list[str]], design: str) -> bool:
    if len(design) == 0:
        return True

    if design in PATTERN_CACHE:
        return PATTERN_CACHE[design]

    for pattern in patterns[design[0]]:
        if design.startswith(pattern):
            if is_pattern_possible(patterns, design[len(pattern) :]):
                PATTERN_CACHE[design] = True
                return True

    PATTERN_CACHE[design] = False
    return False


def get_num_of_pattern_traces(patterns: dict[str, list[str]], design: str) -> bool:
    if len(design) == 0:
        return 1

    if design in PATTERN_TRACE_CACHE:
        return PATTERN_TRACE_CACHE[design]

    num_of_traces = 0
    for pattern in patterns[design[0]]:
        if design.startswith(pattern):
            num_of_traces += get_num_of_pattern_traces(patterns, design[len(pattern) :])

    PATTERN_TRACE_CACHE[design] = num_of_traces
    return num_of_traces


def main() -> None:
    with open("input.txt") as f:
        patterns_raw, designs_raw = f.read().strip().split("\n\n")

        patterns = patterns_raw.split(", ")
        designs = designs_raw.splitlines()

        patterns_dict = defaultdict(list[str])
        for pattern in patterns:
            patterns_dict[pattern[0]].append(pattern)

        print(
            f"Part 1: {sum(is_pattern_possible(patterns_dict, design) for design in designs)}"
        )
        print(
            f"Part 2: {sum([get_num_of_pattern_traces(patterns_dict, design) for design in designs if PATTERN_CACHE[design]])}"
        )


if __name__ == "__main__":
    main()
