#!/bin/env python


def main() -> None:
    with open("input.txt") as f:
        key_lock_raw = [kl.splitlines() for kl in f.read().strip().split("\n\n")]

        keys = list[list[int]]()
        locks = list[list[int]]()

        for kl in key_lock_raw:
            if all([char == "." for char in kl[0]]) and all(
                [char == "#" for char in kl[-1]]
            ):
                key = list[int]()
                for col in range(len(kl[0])):
                    key.append([kl[row][col] for row in range(len(kl))].count("#") - 1)
                keys.append(key)
                continue

            if all([char == "#" for char in kl[0]]) and all(
                [char == "." for char in kl[-1]]
            ):
                lock = list[int]()
                for col in range(len(kl[0])):
                    lock.append([kl[row][col] for row in range(len(kl))].count("#") - 1)
                locks.append(lock)
                continue

        unique_pair = set[tuple[int, int]]()
        for lock_i, lock in enumerate(locks):
            for key_i, key in enumerate(keys):
                fit = True
                for l, k in zip(lock, key):
                    if l + k > 5:
                        fit = False
                        break
                if fit:
                    unique_pair.add((lock_i, key_i))

        print(f"Part 1: {len(unique_pair)}")



if __name__ == "__main__":
    main()
