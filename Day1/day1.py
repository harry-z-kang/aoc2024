#!/bin/env python

def main() -> None:
    with open("input.txt", "r") as f:
        data = [[int(n) for n in l.split('   ')] for l in f.readlines()]

        left = [d[0] for d in data]
        right = [d[1] for d in data]

        left.sort()
        right.sort()

        print(f"Part 1: {sum([abs(l - r) for l, r in zip(left, right)])}")

        occurance = {l: 0 for l in set(left)}
        for r in right:
            if r in occurance:
              occurance[r] += 1

        print(f"Part 2: {sum([l * occurance[l] for l in left])}")

if __name__ == "__main__":
    main()
